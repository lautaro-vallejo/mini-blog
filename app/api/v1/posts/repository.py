from typing import Optional, List
from sqlalchemy import select, func
from sqlalchemy.orm import Session, selectinload, joinedload
from app.models import PostORM, TagORM, AuthorORM
from app.services.pagination import paginate_query
from app.api.v1.tags.repository import TagRepository


class PostRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, post_id: int) -> Optional[PostORM]:
        post_find = select(PostORM).where(PostORM.id == post_id)
        return self.db.execute(post_find).scalar_one_or_none()

    def search(self, query: Optional[str], order_by: str, direction: str, page: int, per_page: int) -> dict:
        results = select(PostORM)

        if query:
            results = results.where(PostORM.title.ilike(f"%{query}%"))

        # Módulo 9: usamos la paginación global en lugar de repetir la lógica
        return paginate_query(
            self.db, PostORM, base_query=results,
            page=page, per_page=per_page,
            order_by=order_by, direction=direction,
            allowed_order={"id": PostORM.id,
                           "title": func.lower(PostORM.title)},
        )

    def by_tags(self, tags: List[str]) -> List[PostORM]:
        normalized_tag_names = [tag.strip().lower()
                                for tag in tags if tag.strip()]

        if not normalized_tag_names:
            return []

        post_list = (
            select(PostORM)
            .options(
                selectinload(PostORM.tags),
                joinedload(PostORM.author),
            ).where(PostORM.tags.any(func.lower(TagORM.name).in_(normalized_tag_names)))
            .order_by(PostORM.id.asc())
        )

        return self.db.execute(post_list).scalars().all()

    def ensure_author(self, name: str, email: str) -> AuthorORM:

        author_obj = self.db.execute(
            select(AuthorORM).where(AuthorORM.email == email)
        ).scalar_one_or_none()

        if author_obj:
            return author_obj

        author_obj = AuthorORM(name=name,
                               email=email)
        self.db.add(author_obj)
        self.db.flush()

        return author_obj

    def ensure_tag(self, name: str) -> TagORM:
        # Delegamos en el repositorio aislado de Tags (normaliza con strip().lower())
        return TagRepository(self.db).ensure_tag(name)

    def create_post(self, title: str, content: str, author: Optional[dict], tags: List[dict], image_url: str) -> PostORM:
        author_obj = None
        if author:
            author_obj = self.ensure_author(
                author["username"], author["email"])

        post = PostORM(title=title, content=content, image_url=image_url,
                       author=author_obj)
        # Fix Módulo 9: por si llega "a, b" pegado, lo partimos y normalizamos
        names: List[str] = []
        for tag in tags:
            for part in tag["name"].split(","):
                name = part.strip().lower()
                if name and name not in names:
                    names.append(name)
        for name in names:
            post.tags.append(self.ensure_tag(name))

        self.db.add(post)
        self.db.flush()
        self.db.refresh(post)
        return post

    def update_post(self, post: PostORM, updates: dict) -> PostORM:
        for key, value in updates.items():
            setattr(post, key, value)

        return post

    def delete_post(self, post: PostORM) -> None:
        self.db.delete(post)
