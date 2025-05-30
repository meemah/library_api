from pydantic import BaseModel
from typing import Optional
class CreateGenreSchema(BaseModel):
    description:Optional[str]
    name:str
    
class UpdateGenreSchema(BaseModel):
    description:Optional[str]
    name:Optional[str]