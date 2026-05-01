from fastapi import Depends
from sqlalchemy.orm import Session

from app.component.category.repository import CategoryRepository
from app.component.database.database import get_db
from app.component.product.product import Product
from app.component.product.schema import ProductSearch



class Search:
    def __init__(self, db: Session = Depends(get_db), category_repository: CategoryRepository = Depends()):
        self.db = db
        self.category_repository = category_repository

    def search(self, product_search: ProductSearch) -> list[Product]:
        #In a more complex system, this would be handled by ElasticSearch/Algolia or similar
        #We leverage the full-text index created in the Product
        query = self.db.query(Product)
        if product_search.category_id:
            query = query.filter(
                Product.category_id.in_(self.category_repository.get_all_children_ids(product_search.category_id))
            )
        if product_search.price_min is not None:
            query = query.filter(Product.price >= product_search.price_min)
        if product_search.price_max:
            query = query.filter(Product.price <= product_search.price_max)
        if product_search.title:
            # Title is sanitized to alphanumerics + whitespace by ProductSearch
            # so it is safe to feed to MySQL's boolean-mode FT parser.
            query = query.filter(Product.title.match(f"{product_search.title}*", mysql_boolean_mode=True))
        if product_search.sku:
            query = query.filter(Product.sku == product_search.sku)
        return query.all()