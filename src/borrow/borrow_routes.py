

from fastapi import APIRouter,Depends
from src.utils.response.success import SuccessResponse

from src.db.main import get_session
from src.utils.token_bearer import get_user

from src.db.models import BookModel, LoanStatus, UserModel
from typing import List
from .borrow_service import BorrowService


borrow_router = APIRouter()
borrow_service = BorrowService()

@borrow_router.get("/user/borrow_history")
async def get_users_borrow_history(
    session = Depends(get_session),
    loan_status: LoanStatus = LoanStatus.active,
    user: UserModel = Depends(get_user),
    
):
    results = await borrow_service.get_user_borrowed_history(
        session,
        loan_status,
        user.uid   
    )
    return SuccessResponse(
        message="User Borrowing History Fetched",
        data = results
    )
@borrow_router.get("/history")
async def get_users_borrow_history(
    session = Depends(get_session),
    loan_status: LoanStatus = LoanStatus.active,
    
):
    results = await borrow_service.get_all_borrowed_history(
        session,
        loan_status,
    )
    return SuccessResponse(
        message="Borrowing History Fetched",
        data = results
    )
@borrow_router.get("book/{book_uid}/history")
async def get_users_borrow_history(
    book_uid:str,
    session = Depends(get_session),
    
):
    results = await borrow_service.get_book_loan_history(
        session,
        book_uid,
    )
    return SuccessResponse(
        message="Borrowing History Fetched",
        data = results
    )

# @borrow_router.post
