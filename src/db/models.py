from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime,timedelta
from enum import Enum
from typing import Optional, List

class UserRole(str, Enum):
    admin = "admin"
    user = "user"

class LoanStatus(str, Enum):
    active = "active"
    returned = "returned"
    overdue = "overdue"
    lost = "lost"
class AuthorBookLink(SQLModel,table = True):
    author_uid: uuid.UUID = Field(foreign_key="author.uid", primary_key=True)
    book_uid: uuid.UUID = Field(foreign_key="book.uid", primary_key=True)

class GenreBookLink(SQLModel, table=True):
    genre_uid: uuid.UUID = Field(foreign_key="genre.uid",primary_key=True)
    book_uid: uuid.UUID = Field(foreign_key="book.uid", primary_key=True)
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
    reviews: List["ReviewModel"]= Relationship(
        back_populates="user",
  
    )
    loans: List["LoanBookModel"] = Relationship(
        back_populates="user",
      

    )
    loan_queue: List["LoanQueueModel"] = Relationship(
    back_populates="user",
  
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
    books: List["BookModel"] = Relationship(
        link_model=AuthorBookLink,
        back_populates="authors",
     
    )
    

class GenreModel(SQLModel, table=True):
    __tablename__ ="genre"
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        ))
    created_at: datetime = Field(
        sa_column=Column(
        pg.TIMESTAMP,
        nullable=False,
        default= datetime.now
        ))
    updated_at: datetime =Field(
        sa_column=Column(
        pg.TIMESTAMP,
        nullable=False,
        default= datetime.now
        )
    )
    name:str
    description: Optional[str]
    books: List["BookModel"] = Relationship(
          link_model=GenreBookLink,
          back_populates="genres"
    )

    
class BookModel(SQLModel, table=True):
    __tablename__ = "book"
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        ))
    name:str
    published_year: Optional[str]
    description:str
    created_at: datetime = Field(
        sa_column=Column(
        pg.TIMESTAMP,
        nullable=False,
        default= datetime.now
        ))
    updated_at: datetime =Field(
        sa_column=Column(
        pg.TIMESTAMP,
        nullable=False,
        default= datetime.now))
    total_copies: int
    loaned_copies: int = Field(
        default=0)
    authors: List["AuthorModel"] = Relationship(
        link_model=AuthorBookLink,
        back_populates="books",
         sa_relationship_kwargs={"lazy": "noload"})
    genres: List["GenreModel"] = Relationship(
        link_model=GenreBookLink,
        back_populates="books",
         sa_relationship_kwargs={"lazy": "noload"})
    reviews: List["ReviewModel"]= Relationship(
        back_populates="book",
         sa_relationship_kwargs={"lazy": "noload"})
    loans: List["LoanBookModel"] = Relationship(
        back_populates="book",
         sa_relationship_kwargs={"lazy": "noload"})
    loan_queue: List["LoanQueueModel"] = Relationship(
    back_populates="book",
     sa_relationship_kwargs={"lazy": "noload"})
    
    
    
class ReviewModel(SQLModel, table = True):
    __tablename__ = "review"
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    rating: int = Field(
        lt=5
    )
    review: str
    created_at: datetime = Field(
        sa_column=Column(
        pg.TIMESTAMP,
        nullable=False,
        default= datetime.now
        )
    )
    user_uid: uuid.UUID = Field(
        foreign_key="user.uid",
        default=None,

    )
    user: Optional["UserModel"] = Relationship(
        back_populates="reviews",
   
    )
    book_uid: uuid.UUID = Field(
        default=None,
        foreign_key="book.uid",
    )
    book: Optional["BookModel"] = Relationship(
        back_populates="reviews",
      
    )
    

class LoanBookModel(SQLModel, table = True):
    __tablename__ = "loan"
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
    book_uid: uuid.UUID = Field(
        pg.UUID,
        nullable=False,
        foreign_key="book.uid"
    )
    book: Optional["BookModel"] = Relationship(
        back_populates="loans",
     
    )
    user_uid:uuid.UUID = Field(
        pg.UUID,
        nullable=False,
        foreign_key="user.uid"
    )
    user: Optional["UserModel"] = Relationship(
        back_populates="loans",
      
    )
    loan_status: LoanStatus = Field(
        default= LoanStatus.active,
        sa_column=Column(
            pg.TEXT,
            nullable=False
        )
    )
    loan_date: datetime=Field(
        sa_column=Column(
            pg.TIMESTAMP,
            nullable=False,
            default=datetime.now
        )
    )
    due_date: datetime=Field(
        sa_column=Column(
            pg.TIMESTAMP,
            nullable=False,
        )
    )
    return_date: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            pg.TIMESTAMP,
        )
    )
    def __init__(self, **data):
        data.setdefault("due_date", datetime.now() + timedelta(days=14))
        super().__init__(**data)
    
class LoanQueueStatus(str, Enum):
    waiting = "waiting"
    notified = "notified"
    cancelled = "cancelled"
    completed = "completed"
class LoanQueueModel(SQLModel, table=True):
    __tablename__ ="loan_queue"
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    user_uid: uuid.UUID = Field(
              nullable=False,
        foreign_key="user.uid",
      
    )
    user:Optional["UserModel"] = Relationship(
        back_populates="loan_queue",

    )
    book_uid: uuid.UUID = Field(
              foreign_key="book.uid",
                   nullable=False,

    )
    book : Optional["BookModel"]= Relationship(
        back_populates="loan_queue",
      
    )
    joined_at: datetime = Field(
        sa_column=Column(
                    pg.TIMESTAMP,
        nullable=False,
        default=datetime.now
        )

    )
    queue_status: LoanQueueStatus = Field(
        default=LoanQueueStatus.waiting,
        sa_column=Column(
            pg.TEXT,
            nullable=False
        )
    )