from pydantic import BaseModel

class ReviewSchema(BaseModel):
  id: int
  content: str

  class Config:
    orm_mode = True
