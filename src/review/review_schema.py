
from pydantic import BaseModel

class CreateReviewSchema(BaseModel):
    review: str
    rating: int
   
