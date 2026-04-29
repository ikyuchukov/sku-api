from decimal import Decimal
from typing import Optional
from pydantic import BaseModel


class ProductCreate(BaseModel):
    sku: str
    title: str
    description: str
    image: str
    price: Decimal
    category_id: int


class ProductUpdate(BaseModel):
    sku: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    price: Optional[Decimal] = None
    category_id: Optional[int] = None


class ProductResponse(BaseModel):
    id: int
    sku: str
    title: str
    description: str
    image: str
    price: Decimal
    category_id: int

    model_config = {"from_attributes": True}
