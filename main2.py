from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(docs_url="/docs", redoc_url="/redoc")

class Item(BaseModel):
    name: str
    price: int
    is_offer:bool= False
    password: str = "Dont show this"

class ItemResponse(BaseModel):
    name: str
    price: int
    is_offer: bool = False

@app.post("/items/", response_model=ItemResponse)
def create_item(item: Item):
    return {
        # "message": "Item created",
        "item": item
    }