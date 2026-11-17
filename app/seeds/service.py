from contextlib import contextmanager
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.db import Base, SessionLocal, engine
from app.core.security import hash_password
from app.models import CategoryORM, PostORM, TagORM, User
from app.utils.slugify_utils import ensure_unique_slug
from .data import CATEGORIES, POSTS, TAGS, USERS


@contextmanager
def atomic(db: Session):
    """Commit único al terminar o rollback automático si algo falla."""
    try:
        yield
        db.commit()
    except Exception:
        db.rollback()
        raise


# ---------- Búsquedas por clave natural (para el upsert lógico) ----------
def _user_by_email(db: Session, email: str) -> Optional[User]:
    return db.execute(select(User).where(User.email == email)).scalars().first()


def _category_by_slug(db: Session, slug: str) -> Optional[CategoryORM]:
    return db.execute(select(CategoryORM).where(CategoryORM.slug == slug)).scalars().first()


def _tag_by_name(db: Session, name: str) -> Optional[TagORM]:
    return db.execute(select(TagORM).where(func.lower(TagORM.name) == name.lower())).scalars().first()


def _post_by_title(db: Session, title: str) -> Optional[PostORM]:
    return db.execute(select(PostORM).where(PostORM.title == title)).scalars().first()


# ---------- Seeds (idempotentes: se pueden correr muchas veces) ----------
def seed_users(db: Session) -> None:
    with atomic(db):
        for data in USERS:
            obj = _user_by_email(db, data["email"])
            if obj:
                obj.username = data["username"]
                obj.role = data["role"]
            else:
                db.add(User(
                    email=data["email"],
                    username=data["username"],
                    hashed_password=hash_password(data["password"]),
                    role=data["role"],
                ))


def seed_categories(db: Session) -> None:
    with atomic(db):
        for data in CATEGORIES:
            obj = _category_by_slug(db, data["slug"])
            if obj:
                obj.name = data["name"]
            else:
                db.add(CategoryORM(**data))


def seed_tags(db: Session) -> None:
    with atomic(db):
        for name in TAGS:
            if not _tag_by_name(db, name):
                db.add(TagORM(name=name.lower()))


def seed_posts(db: Session) -> None:
    """Requiere usuarios, categorías y tags (por eso run_posts los carga antes)."""
    with atomic(db):
        for data in POSTS:
            category = _category_by_slug(db, data["category"])
            author = _user_by_email(db, data["author"])
            tags = [t for t in (_tag_by_name(db, n) for n in data["tags"]) if t]

            obj = _post_by_title(db, data["title"])
            if obj:
                obj.content = data["content"]
                obj.category = category
                obj.user = author
                obj.tags = tags
            else:
                db.add(PostORM(
                    title=data["title"],
                    slug=ensure_unique_slug(db, data["title"]),
                    content=data["content"],
                    category=category,
                    user=author,
                    tags=tags,
                ))
                db.flush()  # para que el próximo slug vea este


# ---------- Puntos de entrada usados por la CLI ----------
def _session() -> Session:
    Base.metadata.create_all(bind=engine)
    return SessionLocal()


def run_users() -> None:
    with _session() as db:
        seed_users(db)


def run_categories() -> None:
    with _session() as db:
        seed_categories(db)


def run_tags() -> None:
    with _session() as db:
        seed_tags(db)


def run_posts() -> None:
    with _session() as db:
        seed_users(db)
        seed_categories(db)
        seed_tags(db)
        seed_posts(db)


def run_all() -> None:
    run_posts()
