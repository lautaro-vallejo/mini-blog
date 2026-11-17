from typing import Optional

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models import User
from app.services.pagination import paginate_query


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, user_id: int) -> Optional[User]:
        return self.db.get(User, user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        query = select(User).where(func.lower(User.email) == email.lower())
        return self.db.execute(query).scalars().first()

    def get_by_username(self, username: str) -> Optional[User]:
        query = select(User).where(
            func.lower(User.username) == username.lower())
        return self.db.execute(query).scalars().first()

    def list_users(self, search: Optional[str], page: int, per_page: int) -> dict:
        query = select(User)
        if search:
            query = query.where(or_(User.email.ilike(f"%{search}%"),
                                    User.username.ilike(f"%{search}%")))
        return paginate_query(self.db, User, base_query=query,
                              page=page, per_page=per_page)

    def create(self, *, email: str, username: str, password: str, role: str = "user") -> User:
        user = User(email=email.lower(), username=username,
                    hashed_password=hash_password(password), role=role)
        self.db.add(user)
        self.db.flush()
        return user

    def authenticate(self, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    def delete(self, user: User) -> None:
        self.db.delete(user)
