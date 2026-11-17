from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.security import require_role
from app.models import User
from .repository import CategoryRepository
from .schemas import CategoryCreate, CategoryPublic, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=List[CategoryPublic])
def list_categories(db: Session = Depends(get_db)):
    return CategoryRepository(db).list_all()


@router.get("/slug/{slug}", response_model=CategoryPublic)
def get_category_by_slug(slug: str, db: Session = Depends(get_db)):
    category = CategoryRepository(db).get_by_slug(slug)
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return category


@router.get("/{category_id}", response_model=CategoryPublic)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = CategoryRepository(db).get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return category


@router.post("", response_model=CategoryPublic, status_code=status.HTTP_201_CREATED)
def create_category(data: CategoryCreate, db: Session = Depends(get_db),
                    user: User = Depends(require_role("editor"))):
    repository = CategoryRepository(db)
    if repository.get_by_slug(data.slug):
        raise HTTPException(status_code=400, detail="Slug en uso")
    if repository.get_by_name(data.name):
        raise HTTPException(status_code=400, detail="Nombre en uso")

    category = repository.create(name=data.name, slug=data.slug)
    db.commit()
    db.refresh(category)
    return category


@router.patch("/{category_id}", response_model=CategoryPublic)
def update_category(category_id: int, data: CategoryUpdate, db: Session = Depends(get_db),
                    user: User = Depends(require_role("editor"))):
    repository = CategoryRepository(db)
    category = repository.get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    updates = data.model_dump(exclude_unset=True, exclude_none=True)
    if "slug" in updates:
        other = repository.get_by_slug(updates["slug"])
        if other and other.id != category_id:
            raise HTTPException(status_code=400, detail="Slug en uso")
    if "name" in updates:
        other = repository.get_by_name(updates["name"])
        if other and other.id != category_id:
            raise HTTPException(status_code=400, detail="Nombre en uso")

    category = repository.update(category, updates)
    db.commit()
    db.refresh(category)
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db),
                    user: User = Depends(require_role("admin"))):
    repository = CategoryRepository(db)
    category = repository.get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    # Los posts de esta categoría quedan con category_id = NULL (ON DELETE SET NULL)
    repository.delete(category)
    db.commit()
