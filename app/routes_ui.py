from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter(include_in_schema=False)


@router.get("/")
def index():
    return FileResponse("static/index.html")


@router.get("/admin")
def admin():
    return FileResponse("static/admin.html")


@router.get("/ping", include_in_schema=True, tags=["health"])
def ping():
    return {"message": "pong"}
