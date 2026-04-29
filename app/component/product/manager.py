from fastapi import Depends
from sqlalchemy.orm import Session
from app.component.database.database import get_db
from app.component.product.product import Product
from app.component.product.schema import ProductCreate, ProductUpdate


class ProductManager:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create_product(self, product: ProductCreate) -> Product:
        db_product = Product(**product.model_dump())
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def get_product(self, product_id: int) -> Product | None:
        return self.db.get(Product, product_id)

    def get_products(self) -> list[Product]:
        return self.db.query(Product).all()

    def update_product(self, product: ProductUpdate, db_product: Product) -> Product:
        for field in product.model_fields_set:
            setattr(db_product, field, getattr(product, field))
        self.db.commit()
        return db_product

    def delete_product(self, product: Product) -> None:
        self.db.delete(product)
        self.db.commit()
