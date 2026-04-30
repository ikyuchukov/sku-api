from typing import Optional
from pydantic import BaseModel

class CategoryCreate(BaseModel):
    name: str
    parent_id: Optional[int] = None

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    parent_id: Optional[int] = None

class CategoryResponse(BaseModel):
    id: int
    name: str
    parent_id: Optional[int] = None
    children: list["CategoryResponse"] = []

    model_config = {"from_attributes": True}

#Required by Pydantic v2 to resolve the self-referential type.
CategoryResponse.model_rebuild()