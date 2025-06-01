
from pydantic import  BaseModel
from typing import Optional, List
import uuid
from src.db.models import GenreModel, AuthorModel, ReviewModel

class CreateBookSchema(BaseModel):
    name:str
    published_year: Optional[str]
    description:str
    total_copies: int
    authors: Optional[List[uuid.UUID]]
    genres: Optional[List[uuid.UUID]]
    
    class Config:
        orm_mode = True
        
class UpdateBookSchema(BaseModel):
    name:Optional[str] = None
    published_year: Optional[str] = None
    description:Optional[str]= None
    total_copies: Optional[int]= None
    authors: Optional[List[uuid.UUID]]= None
    genres: Optional[List[uuid.UUID]]= None
    
    class Config:
        orm_mode = True


class GetBookSchema(BaseModel):
    name:str
    published_year: Optional[str]
    description:str
    total_copies: int
    loaned_copies:int
    genres: List[GenreModel]
    authors: List[AuthorModel]
    reviews: List[ReviewModel]
    