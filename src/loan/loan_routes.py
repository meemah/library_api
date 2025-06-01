

from fastapi import APIRouter,Depends
from src.utils.response.success import SuccessResponse

from src.db.main import get_session
from src.utils.token_bearer import get_user

from src.db.models import LoanBookModel, LoanStatus, UserModel
from typing import List
from .loan_service import LoanService


loan_router = APIRouter()


@loan_router.get("/user/loan_history")
async def get_users_loan_history(
    session = Depends(get_session),
    loan_status: LoanStatus = LoanStatus.active,
    user: UserModel = Depends(get_user),
    
):
    results = await LoanService.get_user_loan_history(
        session,
        loan_status,
        user.uid   
    )
    return SuccessResponse(
        message="User Loaned History Fetched",
        data = results
    )
@loan_router.get("/history")
async def get_users_loan_history(
    session = Depends(get_session),
    loan_status: LoanStatus = LoanStatus.active,
    
):
    results = await LoanService.get_all_loan_history(
        session,
        loan_status,
    )
    return SuccessResponse(
        message="Loaned History Fetched",
        data = results
    )
@loan_router.get("/book/{book_uid}/history")
async def get_users_loan_history(
    book_uid:str,
    session = Depends(get_session),
    
):
    results = await LoanService.get_book_loan_history(
        session,
        book_uid,
    )
    return SuccessResponse(
        message="Loaned History Fetched",
        data = results
    )

@loan_router.get("/book/{book_uid}/loan",response_model=SuccessResponse[LoanBookModel])
async def borrow_book(
    book_uid:str,
    session = Depends(get_session),
    user: UserModel = Depends(get_user),
):
    loan = await LoanService.borrow_book(
        session,
        user.email,
        book_uid
    )
    
    return SuccessResponse(
        message="Successfully loaned this book",
        data = loan
    )

@loan_router.get("/book/{book_uid}/return",response_model=SuccessResponse[LoanBookModel])
async def borrow_book(
    loan_uid:str,
    session = Depends(get_session),

):
    loan = await LoanService.return_book(
        session,loan_uid
    )
    
    return SuccessResponse(
        message="Successfully loaned this book",
        data = loan
    )
    
    # 6f5c6810-afe1-4f3f-b1ae-ac14321b240a