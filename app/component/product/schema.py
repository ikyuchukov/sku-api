import re
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field, field_validator

# Complete set of MySQL FULLTEXT boolean-mode operators. Everything else
# (including unicode word chars) is left untouched so non-ASCII titles work.
# Reference: https://dev.mysql.com/doc/refman/8.0/en/fulltext-boolean.html
#   +  required term
#   -  forbidden term
#   >  increase relevance
#   <  decrease relevance
#   (  group open
#   )  group close
#   ~  negation (rank-only)
#   *  right-truncation wildcard
#   "  phrase delimiter
#   @  proximity operator (InnoDB)
_FT_BOOLEAN_OPERATORS = re.compile(r'[+\-<>()~*"@]+')


class ProductCreate(BaseModel):
    sku: str = Field(min_length=3)
    title: str = Field(min_length=3)
    description: str = Field(min_length=3)
    image: str = Field(min_length=3)
    price: Decimal = Field(gt=0)
    category_id: int


class ProductUpdate(BaseModel):
    sku: Optional[str] = Field(default=None, min_length = 3)
    title: Optional[str] = Field(default=None, min_length=3)
    description: Optional[str] = Field(default=None, min_length=3)
    image: Optional[str] = Field(default=None, min_length=3)
    price: Optional[Decimal] = Field(default=None, gt=0)
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

class ProductSearch(BaseModel):
    title: Optional[str] = Field(default=None)
    sku: Optional[str] = None
    category_id: Optional[int] = None
    price_min: Optional[Decimal] = Field(default=None, gt=0)
    price_max: Optional[Decimal] = Field(default=None, gt=0)

    @field_validator("title", mode="after")
    @classmethod
    def _sanitize_title(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        sanitized = _FT_BOOLEAN_OPERATORS.sub(" ", value).strip()
        return sanitized or None