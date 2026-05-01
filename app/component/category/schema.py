from typing import Optional
from pydantic import BaseModel, Field

class CategoryCreate(BaseModel):
    name: str = Field(min_length=3)
    parent_id: Optional[int] = None

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3)
    parent_id: Optional[int] = None

class CategoryResponse(BaseModel):
    id: int
    name: str
    parent_id: Optional[int] = None
    children: list["CategoryResponse"] = []

    model_config = {"from_attributes": True}

#Required by Pydantic v2 to resolve the self-referential type.
CategoryResponse.model_rebuild()