from fastapi import FastAPI

class NotFoundException(Exception):
    def __init__(self, name):
        self.name = name

app = FastAPI()

from fastapi.responses import JSONResponse
from fastapi.requests import Request

@app.exception_handler(NotFoundException)
def not_found_exception_handler(request: Request, exec: NotFoundException):
    return JSONResponse (
        status_code=400,
        content = {"message": f"Oops {exec.name} was not found"}
    )

items = {"apple": 10, "orange": 20, "banana": 30}

@app.get("/item/{item_name}")
def get_item(item_name: str):
    if item_name not in items:
        raise NotFoundException(item_name)
    return {"item name" : item_name, "price": items[item_name]} 
