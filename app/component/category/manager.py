from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.component.database.database import get_db
from app.component.category.category import Category
from app.component.category.schema import CategoryCreate, CategoryDto, CategoryUpdate
from app.component.product.product import Product
from app.component.category.exceptions import CategoryCycleError, CategoryNotEmptyError


#Would be separated into multiple services when more complexity arrives
class CategoryManager:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create_category(self, category: CategoryCreate) -> Category:
        db_category = Category(name=category.name, parent_id=category.parent_id)
        self.db.add(db_category)
        self.db.flush()

        return db_category

    def update_category(self, category: CategoryUpdate, db_category: Category) -> Category:
        if "name" in category.model_fields_set:
            db_category.name = category.name
        if "parent_id" in category.model_fields_set:
            new_parent_id = category.parent_id
            if new_parent_id is not None:
                if new_parent_id == db_category.id:
                    raise CategoryCycleError(
                        "A category cannot be it's own parent."
                    )
                if new_parent_id in self.get_all_children_ids(db_category.id):
                    raise CategoryCycleError(
                        "A category cannot be it's own descendant."
                    )
            db_category.parent_id = new_parent_id
        self.db.flush()

        return db_category

    def delete_category(self, category: Category) -> None:
        child_count = (
            self.db.query(Category).filter(Category.parent_id == category.id).count()
        )
        if child_count:
            raise CategoryNotEmptyError(
                f"Category has {child_count} child categories. Re-parent or delete them first."
            )
        product_count = (
            self.db.query(Product).filter(Product.category_id == category.id).count()
        )
        if product_count:
            raise CategoryNotEmptyError(
                f"Category is referenced by {product_count} products re-assign or delete them first."
            )
        self.db.delete(category)
        self.db.flush()

    def get_category(self, category_id: int) -> Category|None:
        return self.db.get(Category, category_id)

    def get_categories(self, parent_id: int|None = None) -> list[Category]:
        return self.db.query(Category).filter(Category.parent_id == parent_id).all()

    def get_all_categories(self) -> list[Category]:
        return self.db.query(Category).all()

    def get_categories_by_ids(self, ids: list[int]) -> list[Category]:
        if not ids:
            return []
        return self.db.query(Category).filter(Category.id.in_(ids)).all()

    def get_all_children_ids(self, category_id: int) -> list[int]:
        # Recursive CTE
        anchor = (
            select(Category.id)
            .where(Category.id == category_id)
            .cte(name="category_tree", recursive=True)
        )
        recursive = select(Category.id).where(Category.parent_id == anchor.c.id)
        tree = anchor.union_all(recursive)
        return list(self.db.execute(select(tree.c.id)).scalars().all())

    @staticmethod
    def build_category_tree(categories: list[Category]) -> list[CategoryDto]:
        #We create a dictionary of categories by id
        nodes: dict[int, CategoryDto] = {
            c.id: CategoryDto(id=c.id, name=c.name, parent_id=c.parent_id, children=[])
            for c in categories
        }
        roots: list[CategoryDto] = []
        for node in nodes.values():
            #We get the parent for the node if it exists
            parent = nodes.get(node.parent_id) if node.parent_id is not None else None
            if parent is None:
                #If no parent, we append as root
                roots.append(node)
            else:
                #If parent exists, we append CURRENT node as child
                parent.children.append(node)
        return roots