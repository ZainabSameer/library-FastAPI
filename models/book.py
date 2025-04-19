from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship  # Import the relationship 
from .base import BaseModel  # Import the base model for SQLAlchemy


class BookModel(BaseModel):

    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    author = Column(String)
    in_stock = Column(Boolean)
    rating = Column(Integer)
    publication_year = Column(Integer)

