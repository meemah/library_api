
from pydantic import BaseModel, Field
import uuid
from datetime import datetime
class CreateReviewSchema(BaseModel):
    review: str 
    rating: int = Field(
        lt=5
    )
   
class GetReviewSchema(BaseModel):
    review: str
    rating: int
    uid: uuid.UUID 
    created_at: datetime
   
