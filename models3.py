from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database2 import Base

class User(Base):
    __tablename__ = "Users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)