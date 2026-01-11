from sqlmodel import SQLModel, Field
from typing import Optional
from contextlib import asynccontextmanager

class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: int
    is_offer: bool=True

from sqlmodel import create_engine, Session

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True) 

def create_db_tables():
    SQLModel.metadata.create_all(engine)

from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    #startup
    create_db_tables()
    yield
    #shutdown
    

app = FastAPI(lifespan=lifespan)

from fastapi import Depends

@app.post("/items/")
def create_item(item: Item):
    with Session(engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item 

from typing import List
from sqlmodel import select

@app.get("/items/", response_model=List[Item])
def read_items():
    with Session (engine) as session:
        items = session.exec(select(Item)).all()
        return items