from fastapi import FastAPI, Depends
from fastapi.exceptions import HTTPException

from app.component.category.manager import CategoryManager
from app.component.category.schema import CategoryCreate, CategoryResponse, CategoryUpdate

app = FastAPI()


@app.get("/ping")
def root():
    return {"message": "pong"}

@app.post("/product")
async def create_product():

    return {"message": "Product created"}

@app.post("/category", response_model=CategoryResponse)
async def create_category(category: CategoryCreate, manager: CategoryManager = Depends()) -> CategoryResponse:
    return manager.create_category(category)

@app.patch("/category/{category_id}", response_model=CategoryResponse)
async def update_category(category_id: int, category: CategoryUpdate, manager: CategoryManager = Depends()) -> CategoryResponse:
    db_category = manager.get_category(category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return manager.update_category(category, db_category)

@app.delete("/category/{category_id}", status_code=204)
async def delete_category(category_id: int, manager: CategoryManager = Depends()):
    db_category = manager.get_category(category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    manager.delete_category(db_category)

@app.get("/category", response_model=list[CategoryResponse])
async def get_categories(manager: CategoryManager = Depends()) -> list[CategoryResponse]:
    return manager.get_categories()

@app.get("/category/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int, manager: CategoryManager = Depends()) -> CategoryResponse:
    category = manager.get_category(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category
