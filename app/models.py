from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from .database import Base

class Note(Base):

    __tablename__ = "stickynote"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)