from fastapi import Depends

from app.component.category.exceptions import CategoryNotFoundError
from app.component.category.repository import CategoryRepository
from app.component.product.exceptions import DuplicateSkuError
from app.component.product.product import Product
from app.component.product.repository import ProductRepository
from app.component.product.schema import ProductCreate, ProductUpdate


class ProductManager:
    def __init__(self, repository: ProductRepository = Depends(), category_repository: CategoryRepository = Depends()):
        self.repository = repository
        self.category_repository = category_repository

    def create_product(self, product: ProductCreate) -> Product:
        self._ensure_sku_available(product.sku)
        self._ensure_category_exists(product.category_id)

        db_product = Product()
        for field in product.model_fields_set:
            setattr(db_product, field, getattr(product, field))
        self.repository.db.add(db_product)
        self.repository.db.flush()
        return db_product

    def update_product(self, product: ProductUpdate, db_product: Product) -> Product:
        fields = product.model_fields_set
        if "sku" in fields and product.sku != db_product.sku:
            self._ensure_sku_available(product.sku)
        if "category_id" in fields and product.category_id != db_product.category_id:
            self._ensure_category_exists(product.category_id)

        for field in fields:
            setattr(db_product, field, getattr(product, field))
        self.repository.db.flush()
        return db_product

    def delete_product(self, product: Product) -> None:
        self.repository.db.delete(product)
        self.repository.db.flush()

    def _ensure_sku_available(self, sku: str) -> None:
        if self.repository.get_product_by_sku(sku):
            raise DuplicateSkuError(f"A product with sku {sku!r} already exists.")

    def _ensure_category_exists(self, category_id: int) -> None:
        if not self.category_repository.get_category(category_id):
            raise CategoryNotFoundError(f"category_id {category_id} does not exist.")
