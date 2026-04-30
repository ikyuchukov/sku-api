from fastapi import Depends
from sqlalchemy.orm import Session
from app.component.database.database import get_db
from app.component.category.category import Category
from app.component.category.schema import CategoryCreate, CategoryUpdate

#Would be separated into multiple services when more complexity arrives
class CategoryManager:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create_category(self, category: CategoryCreate) -> Category:
        db_category = Category(name=category.name, parent_id=category.parent_id)
        self.db.add(db_category)
        self.db.commit()
        self.db.refresh(db_category)

        return db_category

    def update_category(self, category: CategoryUpdate, db_category: Category) -> Category:
        if "name" in category.model_fields_set:
            db_category.name = category.name
        if "parent_id" in category.model_fields_set:
            db_category.parent_id = category.parent_id
        self.db.commit()

        return db_category

    def delete_category(self, category: Category) -> bool:
        self.db.delete(category)
        self.db.commit()

        return True

    def get_category(self, category_id: int) -> Category|None:
        return self.db.get(Category, category_id)

    def get_categories(self, parent_id: int|None = None) -> list[Category]:
        return self.db.query(Category).filter(Category.parent_id == parent_id).all()

    def get_all_children_ids(self, category_id: int) -> list[int]:
        ids = [category_id]
        for child_category in self.get_categories(category_id):
            ids.extend(self.get_all_children_ids(child_category.id))

        return ids