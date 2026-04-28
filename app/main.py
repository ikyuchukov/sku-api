from fastapi import FastAPI, Depends

from app.component.category.manager import CategoryManager
from app.component.category.schema import CategoryCreate, CategoryResponse

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello from app!"}

@app.post("/product")
async def create_product():

    return {"message": "Product created"}

@app.post("/category", response_model=CategoryResponse)
async def create_category(category: CategoryCreate, manager: CategoryManager = Depends()) -> CategoryResponse:
    return manager.create_category(category)

@app.get("/category", response_model=list[CategoryResponse])
async def get_categories(manager: CategoryManager = Depends()) -> list[CategoryResponse]:
    return manager.get_categories()

@app.get("/category/{category_id}", response_model=CategoryResponse)
async def _get_category(category_id: int, manager: CategoryManager = Depends()) -> CategoryResponse:
    return manager.get_category(category_id)