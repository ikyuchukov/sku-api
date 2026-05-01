from fastapi import Depends
from sqlalchemy.orm import Session
from app.component.category.category import Category
from app.component.database.database import get_db
from app.component.product.product import Product
from app.component.product.schema import ProductCreate, ProductUpdate
from app.component.category.exceptions import CategoryNotFoundError
from app.component.product.exceptions import DuplicateSkuError

#Would be separated into multiple services when more complexity arrives
class ProductManager:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create_product(self, product: ProductCreate) -> Product:
        self._ensure_sku_available(product.sku)
        self._ensure_category_exists(product.category_id)

        db_product = Product()
        for field in product.model_fields_set:
            setattr(db_product, field, getattr(product, field))
        self.db.add(db_product)
        self.db.flush()
        return db_product

    def get_product(self, product_id: int) -> Product | None:
        return self.db.get(Product, product_id)

    def get_products(self) -> list[Product]:
        return self.db.query(Product).all()

    def update_product(self, product: ProductUpdate, db_product: Product) -> Product:
        fields = product.model_fields_set
        if "sku" in fields and product.sku != db_product.sku:
            self._ensure_sku_available(product.sku)
        if "category_id" in fields and product.category_id != db_product.category_id:
            self._ensure_category_exists(product.category_id)

        for field in fields:
            setattr(db_product, field, getattr(product, field))
        self.db.flush()
        return db_product

    def delete_product(self, product: Product) -> None:
        self.db.delete(product)
        self.db.flush()

    def _ensure_sku_available(self, sku: str) -> None:
        exists = self.db.query(Product.id).filter(Product.sku == sku).first()
        if exists:
            raise DuplicateSkuError(f"A product with sku {sku!r} already exists.")

    def _ensure_category_exists(self, category_id: int) -> None:
        if not self.db.get(Category, category_id):
            raise CategoryNotFoundError(f"category_id {category_id} does not exist.")
