from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello from app!"}

@app.post("/product")
def create_product():

    return {"message": "Product created"}

