postgress_uri = "postgresql://postgres:Ig2sUiQRAvbeSFMY@db.zwisimdzrjafjukockqp.supabase.co:5432/postgres"


from sqlmodel import SQLModel, Field, select
from contextlib import asynccontextmanager
from typing import Optional

class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    is_offer: bool=False

from sqlmodel import create_engine, Session

engine = create_engine(postgress_uri, echo=True)

from fastapi import FastAPI
from contextlib import asynccontextmanager

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# @asynccontextmanager
# def lifespan(app: FastAPI):
#     #startup
#     create_db_and_tables()
#     yield
#     #shutdown

# from contextlib import asynccontextmanager

# @asynccontextmanager
# async def lifespan(app):
#     # Startup logic
#     print("Application startup")
#     yield
#     # Shutdown logic
#     print("Application shutdown")

@asynccontextmanager
async def lifespan(app):
    # Startup logic
    print("Application startup")
    create_db_and_tables()  # Create tables during startup
    yield
    # Shutdown logic
    print("Application shutdown")

app = FastAPI(lifespan=lifespan)

@app.post("/items/")
def create_item(item: Item):
    with Session(engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)
    return item

# app = FastAPI(lifespan=lifespan)

# @app.post("/items/")
# def create_item(item: Item):
#     with Session(engine) as session:
#         session.add(item)
#         session.commit()
#         session.refresh(item)
#         return item
    
from typing import List

@app.get("/items", response_model=List[Item])
def read_items():
    with Session (engine) as session:
        items = session.exec(select(Item)).all()
        return items

