from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.security import create_access_token, get_current_user
from app.models import User
from app.api.v1.users.repository import UserRepository
from app.api.v1.users.schemas import UserCreate, UserLogin, UserPublic
from .schemas import Token

router = APIRouter(prefix="/auth", tags=["auth"])


def _issue_token(db: Session, email: str, password: str) -> dict:
    user = UserRepository(db).authenticate(email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"})
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Usuario inactivo")

    # sub = id del usuario (siempre string en JWT)
    return {"access_token": create_access_token(sub=str(user.id)),
            "token_type": "bearer"}


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db: Session = Depends(get_db)):
    repository = UserRepository(db)
    if repository.get_by_email(data.email):
        raise HTTPException(status_code=409, detail="El email ya está registrado")
    if repository.get_by_username(data.username):
        raise HTTPException(status_code=409, detail="El username ya está en uso")

    # Todo registro público arranca con rol "user"
    user = repository.create(email=data.email, username=data.username,
                             password=data.password)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login con formulario (lo usa el botón Authorize de /docs).
    En el campo `username` va el email."""
    return _issue_token(db, form_data.username, form_data.password)


@router.post("/login/json", response_model=Token)
def login_json(data: UserLogin, db: Session = Depends(get_db)):
    """Login con JSON (email + password), pensado para un frontend."""
    return _issue_token(db, data.email, data.password)


@router.get("/me", response_model=UserPublic)
def read_me(current: User = Depends(get_current_user)):
    return current
