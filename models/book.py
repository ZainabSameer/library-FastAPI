from sqlalchemy import Column, Integer, String, Boolean , ForeignKey
from sqlalchemy.orm import relationship  
from .base import BaseModel  
from .user import UserModel
from .reviews import ReviewModel



class BookModel(BaseModel):

    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    author = Column(String)
    in_stock = Column(Boolean)
    rating = Column(Integer)
    publication_year = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("UserModel", back_populates="books")
    reviews = relationship("ReviewModel", back_populates="book", cascade="all, delete")


