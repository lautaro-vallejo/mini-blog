from __future__ import annotations
from typing import List, TYPE_CHECKING
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base

if TYPE_CHECKING:
    from .post import PostORM


class CategoryORM(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(60), unique=True, index=True)
    slug: Mapped[str] = mapped_column(String(60), unique=True, index=True)

    # passive_deletes=True: al borrar una categoría dejamos que la base de datos
    # aplique ON DELETE SET NULL en posts.category_id (los posts NO se borran).
    # Por eso no usamos cascade "delete" acá: borraría los posts desde el ORM.
    posts: Mapped[List["PostORM"]] = relationship(
        "PostORM",
        back_populates="category",
        passive_deletes=True
    )
