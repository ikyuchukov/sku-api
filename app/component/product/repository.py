from fastapi import Depends
from sqlalchemy.orm import Session

from app.component.database.database import get_db
from app.component.product.product import Product


class ProductRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_product(self, product_id: int) -> Product | None:
        return self.db.get(Product, product_id)

    def get_products(self) -> list[Product]:
        return self.db.query(Product).all()

    def get_product_by_sku(self, sku: str) -> Product | None:
        return self.db.query(Product).filter(Product.sku == sku).first()
