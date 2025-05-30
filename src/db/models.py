from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime
from enum import Enum
from typing import Optional
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
        pg.TEXT,
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

class AuthorModel(SQLModel, table = True):
    __tablename__ = "author"
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            default=uuid.uuid4,
            primary_key=True
        )
    )
    name: str
    created_at: datetime = Field(
        sa_column=Column(
        pg.TIMESTAMP,
        nullable=False,
        default= datetime.now
        )
    )
    updated_at: datetime =Field(
        sa_column=Column(
        pg.TIMESTAMP,
        nullable=False,
        default= datetime.now
        )
    )
    bio: Optional[str]
    

class GenreModel(SQLModel, table=True):
    __tablename__ ="Genres"
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    created_at: datetime = Field(
        sa_column=Column(
        pg.TIMESTAMP,
        nullable=False,
        default= datetime.now
        )
    )
    updated_at: datetime =Field(
        sa_column=Column(
        pg.TIMESTAMP,
        nullable=False,
        default= datetime.now
        )
    )
    name:str
    description: Optional[str]
    

    