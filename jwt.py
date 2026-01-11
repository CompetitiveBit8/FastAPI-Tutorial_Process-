from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from database2 import SessionLocal, engine, Base
from models3 import User
from auth_utils import verify_password, hash_password, create_access_token, decode_access_token
from pydantic import BaseModel
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

Base.metadata.create_all(bind=engine)

app = FastAPI()
security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
class UserCreate(BaseModel):
    username: str
    password: str
    
@app.post("/signup:")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User created successfully", "id": new_user.id}

@app.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invaid credentials")
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token type": "bearer", "user": db_user}

from typing import Optional
from fastapi import Header, HTTPException, status 

@app.get("/protected")
def protected_route(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials:
        raise HTTPException(status_code=status.HTTP_403_UNAUTHORISED, detiail = "Creds missing")
    token = credentials.credentials
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired token")
    return {"message": "Protected route acessed", "user": payload["sub"]}