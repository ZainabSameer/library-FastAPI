from pydantic import BaseModel
from typing import Optional

class BookSchema(BaseModel):
    id: Optional[int] = None  # Optional ID field

    title: str  # Correct annotation
    author: str  # Correct annotation
    in_stock: bool  # Correct annotation
    rating: int  # Correct annotation
    publication_year: Optional[int] = None  # Correct annotation

    class Config:
        from_attributes = True  # Update from orm_mode to from_attributes