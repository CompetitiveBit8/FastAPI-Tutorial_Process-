from fastapi import FastAPI

app = FastAPI()

text_posts = {}

@app.get("/")
def root():
    return {"Hello" : "World"}

@app.get("/home")
def home():
    return {"Hello":"Man"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str=None):
    return {"item_id" : item_id, "query": q}

@app.get("/products/")
def list_products(skip: int = 0, limit: int = 10):
    return {"skip" : skip, "limit": limit}