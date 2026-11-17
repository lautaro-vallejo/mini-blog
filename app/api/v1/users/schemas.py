from typing import List, Literal, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field

Role = Literal["user", "editor", "admin"]


class UserCreate(BaseModel):
    """Entrada del registro: trae la contraseña en texto plano."""
    email: EmailStr = Field(..., examples=["hincha@mdpfutbolera.com"])
    username: str = Field(..., min_length=3, max_length=50,
                          pattern=r"^[a-zA-Z0-9_.-]+$", examples=["hincha_tiburon"])
    password: str = Field(..., min_length=8, max_length=128)


class UserLogin(BaseModel):
    """Solo email y password para generar el token."""
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    """Respuesta segura: nunca incluye la contraseña."""
    id: int
    email: EmailStr
    username: str
    role: Role
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class UserRoleUpdate(BaseModel):
    role: Role


class UserStatusUpdate(BaseModel):
    is_active: bool


class PaginatedUsers(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    has_prev: bool
    has_next: bool
    search: Optional[str] = None
    items: List[UserPublic]
