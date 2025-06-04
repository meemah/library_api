from pydantic import BaseModel, Field, EmailStr
import uuid
from src.db.models import UserRole

class UserSchema(BaseModel):
    uid:uuid.UUID 
    role: UserRole
    email:str
    username:str 
    first_name:str
    last_name:str
    

class UserCreateSchema(BaseModel):
    role: UserRole
    email:EmailStr 
    username:str = Field(
        min_length=3
    )
    first_name:str
    last_name:str
    password:str = Field(
        min_length=6
    )

class UserLoginSchema(BaseModel):
    email:str
    password:str