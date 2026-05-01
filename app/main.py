from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.component.category.exceptions import (
    CategoryCycleError,
    CategoryNotEmptyError,
    CategoryNotFoundError,
)
from app.component.category.routes import router as category_router
from app.component.product.exceptions import DuplicateSkuError
from app.component.product.routes import router as product_router
from app.routes_ui import router as ui_router

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


_DOMAIN_ERROR_STATUS: dict[type, int] = {
    CategoryCycleError: 400,
    CategoryNotEmptyError: 409,
    CategoryNotFoundError: 400,
    DuplicateSkuError: 409,
}


@app.exception_handler(CategoryCycleError)
@app.exception_handler(CategoryNotEmptyError)
@app.exception_handler(CategoryNotFoundError)
@app.exception_handler(DuplicateSkuError)
async def _handle_domain_error(_: Request, exc: Exception) -> JSONResponse:
    status = _DOMAIN_ERROR_STATUS[type(exc)]
    return JSONResponse(status_code=status, content={"detail": str(exc)})

app.include_router(ui_router)
app.include_router(product_router)
app.include_router(category_router)
