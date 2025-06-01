
from pydantic import BaseModel
import uuid
from datetime import datetime
from src.db.models import BookModel, UserModel, LoanStatus
from typing import Optional

class LoanSchema(BaseModel):
    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime 
    book_uid: uuid.UUID 
    book: Optional[BookModel] = None
    user_uid:uuid.UUID 
    user: Optional[UserModel] = None
    loan_status: LoanStatus
    loan_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None