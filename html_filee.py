from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

app =FastAPI()

Base_dir = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=Base_dir / "templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit", response_class=HTMLResponse)
async def handle_form(request: Request, username: str = Form(...), freq: int = Form(...), age: int = Form(...)):
    context =   {"request": request,
                "username": username,
                "freq": freq,
                "age": age
        }
    return templates.TemplateResponse("result.html", context)