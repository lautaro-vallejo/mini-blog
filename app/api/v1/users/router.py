from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.security import require_role
from app.models import User
from .repository import UserRepository
from .schemas import (PaginatedUsers, UserPublic, UserRoleUpdate,
                      UserStatusUpdate)

# Todo este router es de administración: solo rol admin (nivel 2)
router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=PaginatedUsers)
def list_users(
    search: Optional[str] = Query(None, min_length=1, max_length=50),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    admin: User = Depends(require_role("admin")),
):
    result = UserRepository(db).list_users(search, page, per_page)
    return PaginatedUsers(
        page=result["page"], per_page=per_page, total=result["total"],
        total_pages=result["pages"], has_prev=result["has_prev"],
        has_next=result["has_next"], search=search, items=result["items"],
    )


@router.get("/{user_id}", response_model=UserPublic)
def get_user(user_id: int, db: Session = Depends(get_db),
             admin: User = Depends(require_role("admin"))):
    user = UserRepository(db).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@router.patch("/{user_id}/role", response_model=UserPublic)
def change_role(user_id: int, data: UserRoleUpdate, db: Session = Depends(get_db),
                admin: User = Depends(require_role("admin"))):
    user = UserRepository(db).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if user.id == admin.id and data.role != "admin":
        raise HTTPException(
            status_code=400, detail="No podés quitarte el rol de admin a vos mismo")
    user.role = data.role
    db.commit()
    db.refresh(user)
    return user


@router.patch("/{user_id}/status", response_model=UserPublic)
def change_status(user_id: int, data: UserStatusUpdate, db: Session = Depends(get_db),
                  admin: User = Depends(require_role("admin"))):
    user = UserRepository(db).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if user.id == admin.id:
        raise HTTPException(
            status_code=400, detail="No podés desactivar tu propia cuenta")
    user.is_active = data.is_active
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db),
                admin: User = Depends(require_role("admin"))):
    repository = UserRepository(db)
    user = repository.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if user.id == admin.id:
        raise HTTPException(
            status_code=400, detail="No podés eliminar tu propia cuenta")
    repository.delete(user)
    db.commit()
