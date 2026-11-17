from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.db import get_db
from app.models import User

# ---------------------------------------------------------------------------
# Cifrado de contraseñas con pwdlib (Argon2 recomendado)
# ---------------------------------------------------------------------------
password_hash = PasswordHash.recommended()


def hash_password(plain: str) -> str:
    return password_hash.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return password_hash.verify(plain, hashed)


# ---------------------------------------------------------------------------
# Tokens JWT
# ---------------------------------------------------------------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

credentials_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="No autenticado",
    headers={"WWW-Authenticate": "Bearer"}
)


def raise_expired_token():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token expirado",
        headers={"WWW-Authenticate": "Bearer"}
    )


def raise_forbidden():
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="No tienes permisos suficientes",
    )


def create_access_token(sub: str, minutes: Optional[int] = None) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return jwt.encode(
        {"sub": sub, "exp": expire},
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALG
    )


def decode_token(token: str) -> dict:
    return jwt.decode(
        token,
        settings.JWT_SECRET,
        algorithms=[settings.JWT_ALG]
    )


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = decode_token(token)
    except ExpiredSignatureError:
        raise raise_expired_token()
    except InvalidTokenError:
        raise credentials_exc

    sub: Optional[str] = payload.get("sub")
    if not sub or not sub.isdigit():
        raise credentials_exc

    user = db.get(User, int(sub))
    if not user or not user.is_active:
        raise credentials_exc
    return user


# ---------------------------------------------------------------------------
# Jerarquía de roles: user (0) < editor (1) < admin (2)
# ---------------------------------------------------------------------------
ROLE_LEVEL = {"user": 0, "editor": 1, "admin": 2}


def has_role(user: User, min_role: str) -> bool:
    return ROLE_LEVEL.get(user.role, -1) >= ROLE_LEVEL[min_role]


def require_role(min_role: str):
    """Dependencia: exige que el usuario tenga al menos `min_role`."""
    def _checker(user: User = Depends(get_current_user)) -> User:
        if not has_role(user, min_role):
            raise raise_forbidden()
        return user
    return _checker
