from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship  
from .base import BaseModel  


class BookModel(BaseModel):

    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    author = Column(String)
    in_stock = Column(Boolean)
    rating = Column(Integer)
    publication_year = Column(Integer)

