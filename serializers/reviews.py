from pydantic import BaseModel , ConfigDict
from typing import Optional

class ReviewsSchema(BaseModel):
  id: Optional[int] = None
  content: str

  model_config = ConfigDict(from_attributes=True)
