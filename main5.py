# DB connection URI
postgres_uri = "postgresql://postgres:vnefJjVBtNPABGag@db.xlmfwznzlajevmykjemv.supabase.co:5432/postgres"

# Imports
from sqlmodel import SQLModel, Field, select, create_engine, Session
from typing import Optional, List
from fastapi import FastAPI

# ----- Models -----
class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    is_offer: bool = False

# ----- Engine -----
engine = create_engine(postgres_uri, echo=True)

# ----- Table creation -----
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# ----- FastAPI app -----
app = FastAPI()

# Use startup event to create tables
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# ----- POST endpoint -----
@app.post("/items/", response_model=Item)
def create_item(item: Item):
    with Session(engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item

# ----- GET endpoint -----
@app.get("/items/", response_model=List[Item])
def read_items():
    with Session(engine) as session:
        return session.exec(select(Item)).all()
