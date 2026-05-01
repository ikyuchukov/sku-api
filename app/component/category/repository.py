from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.component.category.category import Category
from app.component.database.database import get_db
from app.component.product.product import Product


class CategoryRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_category(self, category_id: int) -> Category | None:
        return self.db.get(Category, category_id)

    def get_categories(self, parent_id: int | None = None) -> list[Category]:
        return self.db.query(Category).filter(Category.parent_id == parent_id).all()

    def get_all_categories(self) -> list[Category]:
        return self.db.query(Category).all()

    def get_categories_by_ids(self, ids: list[int]) -> list[Category]:
        if not ids:
            return []
        return self.db.query(Category).filter(Category.id.in_(ids)).all()

    def get_all_children_ids(self, category_id: int) -> list[int]:
        anchor = (
            select(Category.id)
            .where(Category.id == category_id)
            .cte(name="category_tree", recursive=True)
        )
        recursive = select(Category.id).where(Category.parent_id == anchor.c.id)
        tree = anchor.union_all(recursive)
        return list(self.db.execute(select(tree.c.id)).scalars().all())

    def get_child_count(self, category_id: int) -> int:
        return self.db.query(Category).filter(Category.parent_id == category_id).count()

    def get_product_count(self, category_id: int) -> int:
        return self.db.query(Product).filter(Product.category_id == category_id).count()
