from typing import Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.security import require_role
from app.models import User
from .repository import TagRepository
from .schemas import (PaginatedTags, TagCreate, TagPublic, TagUpdate,
                      TagWithCount)

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("", response_model=PaginatedTags)
def list_tags(
    search: Optional[str] = Query(None, min_length=1, max_length=30),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=50),
    order_by: Literal["id", "name"] = Query("id"),
    direction: Literal["asc", "desc"] = Query("asc"),
    db: Session = Depends(get_db),
):
    repository = TagRepository(db)
    result = repository.list_tags(search, page, per_page, order_by, direction)
    return PaginatedTags(
        page=result["page"],
        per_page=per_page,
        total=result["total"],
        total_pages=result["pages"],
        has_prev=result["has_prev"],
        has_next=result["has_next"],
        order_by=order_by,
        direction=direction,
        search=search,
        items=result["items"],
    )


@router.get("/popular", response_model=TagWithCount)
def most_popular_tag(db: Session = Depends(get_db)):
    repository = TagRepository(db)
    row = repository.most_popular()
    if not row:
        raise HTTPException(status_code=404, detail="Todavía no hay tags en uso")
    return row


@router.get("/{tag_id}", response_model=TagPublic)
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    repository = TagRepository(db)
    tag = repository.get(tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag no encontrado")
    return tag


@router.post("", response_model=TagPublic, status_code=status.HTTP_201_CREATED)
def create_tag(tag: TagCreate, db: Session = Depends(get_db),
               user: User = Depends(require_role("editor"))):
    repository = TagRepository(db)
    try:
        tag_created = repository.create_tag(name=tag.name)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    db.commit()
    return tag_created


@router.put("/{tag_id}", response_model=TagPublic)
def update_tag(tag_id: int, data: TagUpdate, db: Session = Depends(get_db),
               user: User = Depends(require_role("editor"))):
    repository = TagRepository(db)
    try:
        tag = repository.update(tag_id, data.name)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    if not tag:
        raise HTTPException(status_code=404, detail="Tag no encontrado")
    db.commit()
    return tag


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(tag_id: int, db: Session = Depends(get_db),
               user: User = Depends(require_role("admin"))):
    repository = TagRepository(db)
    if not repository.delete(tag_id):
        raise HTTPException(status_code=404, detail="Tag no encontrado")
    db.commit()
