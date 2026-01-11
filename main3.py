from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional, List
from fastapi import FastAPI
from contextlib import asynccontextmanager

class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: int
    is_offer: bool=True
    
#create the engine
sqlite_file_name = "database2.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url)

def create_db_tables():
    SQLModel.metadata.create_all(engine)


# create the routers

# @asynccontextmanager
# def lifespan(app: FastAPI):
#     #startup
#     create_db_tables()
#     yield
#     #shutdown
    
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    # Startup logic
    print("Application startup")
    yield
    # Shutdown logic
    print("Application shutdown")
    
app = FastAPI(lifespan=lifespan)

@app.post("/item/")
def create_item(item: Item):
    with Session (engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)
    return item

@app.get("/item/", response_model=List[Item])
def read_items():
    with Session (engine) as session:
        item = session.exec(select(Item)).all()
        return item  
