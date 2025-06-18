from pydantic import BaseModel
from typing import Optional


class CreateAuthorSchema(BaseModel):
    """Schema for creating a new author.

    Attributes:
        name (str): The name of the author.
        bio (Optional[str], optional): A short biography of the author. Defaults to None.
    """    
    name:str
    bio:Optional[str]= None

class UpdateAuthorSchema(BaseModel):
    """
    Schema for updating an existing author's information.

    Attributes:
        name (Optional[str], optional): The updated name of the author. Defaults to None.
        bio (Optional[str], optional): The updated biography of the author. Defaults to None.
    """
    name:Optional[str]= None
    bio:Optional[str]= None
    
    
