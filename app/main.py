from fastapi import FastAPI, Depends
from fastapi.exceptions import HTTPException

from app.component.category.manager import CategoryManager
from app.component.category.schema import CategoryCreate, CategoryResponse, CategoryUpdate
from app.component.product.manager import ProductManager
from app.component.product.schema import ProductCreate, ProductResponse, ProductUpdate

app = FastAPI()


@app.get("/ping")
def root():
    return {"message": "pong"}

@app.post("/product", response_model=ProductResponse)
async def create_product(product: ProductCreate, manager: ProductManager = Depends()) -> ProductResponse:
    return manager.create_product(product)

@app.get("/product", response_model=list[ProductResponse])
async def get_products(manager: ProductManager = Depends()) -> list[ProductResponse]:
    return manager.get_products()

@app.get("/product/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, manager: ProductManager = Depends()) -> ProductResponse:
    product = manager.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.patch("/product/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, product: ProductUpdate, manager: ProductManager = Depends()) -> ProductResponse:
    db_product = manager.get_product(product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return manager.update_product(product, db_product)

@app.delete("/product/{product_id}", status_code=204)
async def delete_product(product_id: int, manager: ProductManager = Depends()):
    db_product = manager.get_product(product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    manager.delete_product(db_product)

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
