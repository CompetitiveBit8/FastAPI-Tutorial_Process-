from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/divide")
def divide(a: float, b: float):
    if b == 0:
        raise HTTPException(status_code=400, detail="Division by zero is not allowed.")
    return {"result": a / b}

class NotFoundException(Exception):
    def __init__(self, name: str):
        self.name=name
        
from fastapi.responses import JSONResponse
from fastapi.requests import Request

@app.exception_handler(NotFoundException)
def not_found_exception_handler(request: Request, exec: NotFoundException):
    return JSONResponse(
        status_code=404,
        content={"message": f"Oops! {exec.name} not found"}
    )
    
items = {"apple": 10, "banana": 20, "orange": 30}
    
@app.get("/items/{item_name}")
def get_item(item_name: str):
    if item_name not in items:
        raise NotFoundException(item_name)
    return {"item_name": item_name, "price": items[item_name]}