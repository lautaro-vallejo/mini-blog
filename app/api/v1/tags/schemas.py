from typing import List, Literal, Optional
from pydantic import BaseModel, ConfigDict, Field


class TagPublic(BaseModel):
    id: int
    name: str = Field(..., min_length=2, max_length=30)

    model_config = ConfigDict(from_attributes=True)


class TagCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=30,
                      examples=["aldosivi"])


class TagUpdate(BaseModel):
    name: str = Field(..., min_length=2, max_length=30)


class TagWithCount(TagPublic):
    uses: int


class PaginatedTags(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    has_prev: bool
    has_next: bool
    order_by: Literal["id", "name"]
    direction: Literal["asc", "desc"]
    search: Optional[str] = None
    items: List[TagPublic]
