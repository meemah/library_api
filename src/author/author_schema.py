from pydantic import BaseModel
from typing import Optional


class CreateAuthorSchema(BaseModel):
    name:str
    bio:Optional[str]= None

class UpdateAuthorSchema(BaseModel):
    name:Optional[str]= None
    bio:Optional[str]= None
    
    
