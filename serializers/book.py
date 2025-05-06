from pydantic import BaseModel
from typing import Optional

class BookSchema(BaseModel):
    id: Optional[int] = None  
    title: str  
    author: str  
    in_stock: bool  
    rating: int  
    publication_year: Optional[int] = None  

    class Config:
        from_attributes = True  

class BookCreate(BaseModel):
    title: str
    author: str
    in_stock: bool
    rating: int
    publication_year: Optional[int] = None