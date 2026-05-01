from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.component.category.manager import CategoryManager
from app.component.category.repository import CategoryRepository
from app.component.category.schema import (
    CategoryCreate,
    CategoryDto,
    CategoryUpdate,
)
from app.component.database.database import get_db

router = APIRouter(prefix="/category", tags=["category"])


@router.post("", response_model=CategoryDto)
async def create_category(
    category: CategoryCreate,
    manager: CategoryManager = Depends(),
    db: Session = Depends(get_db),
) -> CategoryDto:
    db_category = manager.create_category(category)
    db.commit()
    return db_category


@router.get("", response_model=list[CategoryDto])
async def get_categories(repository: CategoryRepository = Depends()) -> list[CategoryDto]:
    return CategoryManager.build_category_tree(repository.get_all_categories())


@router.get("/{category_id}", response_model=CategoryDto)
async def get_category(category_id: int, repository: CategoryRepository = Depends()) -> CategoryDto:
    descendant_ids = repository.get_all_children_ids(category_id)
    if not descendant_ids:
        raise HTTPException(status_code=404, detail="Category not found")
    rows = repository.get_categories_by_ids(descendant_ids)
    return CategoryManager.build_category_tree(rows)[0]


@router.patch("/{category_id}", response_model=CategoryDto)
async def update_category(
    category_id: int,
    category: CategoryUpdate,
    manager: CategoryManager = Depends(),
    repository: CategoryRepository = Depends(),
    db: Session = Depends(get_db),
) -> CategoryDto:
    db_category = repository.get_category(category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    updated = manager.update_category(category, db_category)
    db.commit()
    return updated


@router.delete("/{category_id}", status_code=204)
async def delete_category(
    category_id: int,
    manager: CategoryManager = Depends(),
    repository: CategoryRepository = Depends(),
    db: Session = Depends(get_db),
):
    db_category = repository.get_category(category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    manager.delete_category(db_category)
    db.commit()
