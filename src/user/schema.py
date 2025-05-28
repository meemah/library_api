from pydantic import BaseModel
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
    email:str
    username:str
    first_name:str
    last_name:str
    password:str

class UserLoginSchema(BaseModel):

    email:str
    password:str