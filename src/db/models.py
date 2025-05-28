from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    user = "user"

class UserModel(SQLModel,table=True):
    __tablename__ = "user"
    uid:uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            nullable=False,
            default=uuid.uuid4
        )
    )
    role: UserRole = Field(
        sa_column=Column(
        pg.CHAR,
        default=UserRole.user,
        nullable=False
        )

    )
    email:str
    username:str
    first_name:str
    last_name:str
    is_verified: bool = False
    password:str = Field(
        exclude=True
    )
    created_at:datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default=datetime.now
        )
    )
    updated_at:datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default=datetime.now
        )
    )