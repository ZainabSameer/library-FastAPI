from pydantic import BaseModel , ConfigDict
from typing import Optional , List
#from reviews import ReviewsSchema
from .reviews import ReviewsSchema
from .user import UserResponseSchema
class BookSchema(BaseModel):
    id: Optional[int] = None 
    title: str  
    author: str  
    in_stock: bool  
    rating: int  
    publication_year: Optional[int] = None  
    user: UserResponseSchema
    reviews: List[ReviewsSchema] = []

    model_config = ConfigDict(from_attributes=True)

class BookCreate(BaseModel):
    title: str
    author: str
    in_stock: bool
    rating: int
    publication_year: Optional[int] = None

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    in_stock: Optional[bool] = None
    rating: Optional[int] = None
    publication_year: Optional[int] = None