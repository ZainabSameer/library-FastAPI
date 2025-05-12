from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class ReviewModel(BaseModel):

    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    book = relationship("BookModel", back_populates="reviews")  