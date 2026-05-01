from fastapi import Depends

from app.component.category.category import Category
from app.component.category.exceptions import CategoryCycleError, CategoryNotEmptyError
from app.component.category.repository import CategoryRepository
from app.component.category.schema import CategoryCreate, CategoryDto, CategoryUpdate


class CategoryManager:
    def __init__(self, repository: CategoryRepository = Depends()):
        self.repository = repository

    def create_category(self, category: CategoryCreate) -> Category:
        db_category = Category(name=category.name, parent_id=category.parent_id)
        self.repository.db.add(db_category)
        self.repository.db.flush()
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
                if new_parent_id in self.repository.get_all_children_ids(db_category.id):
                    raise CategoryCycleError(
                        "A category cannot be it's own descendant."
                    )
            db_category.parent_id = new_parent_id
        self.repository.db.flush()
        return db_category

    def delete_category(self, category: Category) -> None:
        child_count = self.repository.get_child_count(category.id)
        if child_count:
            raise CategoryNotEmptyError(
                f"Category has {child_count} child categories. Re-parent or delete them first."
            )
        product_count = self.repository.get_product_count(category.id)
        if product_count:
            raise CategoryNotEmptyError(
                f"Category is referenced by {product_count} products re-assign or delete them first."
            )
        self.repository.db.delete(category)
        self.repository.db.flush()

    @staticmethod
    def build_category_tree(categories: list[Category]) -> list[CategoryDto]:
        nodes: dict[int, CategoryDto] = {
            c.id: CategoryDto(id=c.id, name=c.name, parent_id=c.parent_id, children=[])
            for c in categories
        }
        roots: list[CategoryDto] = []
        for node in nodes.values():
            parent = nodes.get(node.parent_id) if node.parent_id is not None else None
            if parent is None:
                roots.append(node)
            else:
                parent.children.append(node)
        return roots