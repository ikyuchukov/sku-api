from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.component.database.database import get_db
from app.component.product.manager import ProductManager
from app.component.product.repository import ProductRepository
from app.component.product.schema import (
    ProductCreate,
    ProductResponse,
    ProductSearch,
    ProductUpdate,
)
from app.component.product.search import Search

router = APIRouter(prefix="/product", tags=["product"])


@router.post("", response_model=ProductResponse)
async def create_product(
    product: ProductCreate,
    manager: ProductManager = Depends(),
    db: Session = Depends(get_db),
) -> ProductResponse:
    db_product = manager.create_product(product)
    db.commit()
    return db_product


@router.get("", response_model=list[ProductResponse])
async def get_products(
    product_search: ProductSearch = Depends(),
    search: Search = Depends(),
) -> list[ProductResponse]:
    return search.search(product_search)


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, repository: ProductRepository = Depends()) -> ProductResponse:
    product = repository.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.patch("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product: ProductUpdate,
    manager: ProductManager = Depends(),
    repository: ProductRepository = Depends(),
    db: Session = Depends(get_db),
) -> ProductResponse:
    db_product = repository.get_product(product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    updated = manager.update_product(product, db_product)
    db.commit()
    return updated


@router.delete("/{product_id}", status_code=204)
async def delete_product(
    product_id: int,
    manager: ProductManager = Depends(),
    repository: ProductRepository = Depends(),
    db: Session = Depends(get_db),
):
    db_product = repository.get_product(product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    manager.delete_product(db_product)
    db.commit()
