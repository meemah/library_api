
from pydantic import BaseModel
import uuid
from datetime import datetime
class CreateReviewSchema(BaseModel):
    review: str
    rating: int
   
class GetReviewSchema(BaseModel):
    review: str
    rating: int
    uid: uuid.UUID 
    created_at: datetime
   
