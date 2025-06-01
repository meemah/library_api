from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select,desc
from src.db.models import BorrowBookModel, LoanStatus
from src.book.book_service import BookService
from src.user.user_service import UserService
from src.utils.response.error import BookNotFound, UserNotFound, BorrowBookNotAvailable, UserBorrowedBookAlready, LoanNotFound, BookNotOnLoan
from datetime import datetime

book_service = BookService()
user_service = UserService()

class BorrowService:
    @staticmethod
    async def borrow_book(
        session: AsyncSession,
        user_email: str,
        book_uid: str  
    ):
        book = await book_service.get_book(session, book_uid)
        if book is None:
            raise BookNotFound()
        user = await user_service.get_user(session, user_email)
        if user is None:
            return UserNotFound()
        total_copies: int = book.total_copies
        
        if total_copies <=0 or total_copies == book.borrowed_copies:
            raise BorrowBookNotAvailable()
        has_exisitng_loan = await BorrowService.get_user_borrowed_history (
            session,
            LoanStatus.active,
            user_uid=user.uid
        )
        if has_exisitng_loan:
            raise UserBorrowedBookAlready()
        book.borrowed_copies += 1
        
        borrowed = BorrowBookModel(
            book_uid =book.uid,
            user_uid = user.uid,
            user = user,
            book = book
        )
        
        session.add(borrowed)
        await session.commit()
        await session.refresh(borrowed)
        return borrowed
        
    
    @staticmethod
    async def return_book(
        session:AsyncSession, 
        loan_uid:str,
    ):
        
        loan =  await BorrowService.get_borrow_details(session, loan_uid)
        if loan is None:
            raise LoanNotFound()
        else: 
            if loan.loan_status != LoanStatus.active:
                return BookNotOnLoan()
            else:
                loan.return_date = datetime.now()
                loan.loan_status = LoanStatus.returned
                
                book = await BookService.get_book(session, loan.book_uid)
                if book is None:
                    return BookNotFound()
                else: 
                    book.borrowed_copies -=1
                    await session.commit()
                    await session.refresh(loan)
                    return loan
            
        
        
    @staticmethod 
    async def  get_borrow_details(
        session:AsyncSession, 
        loan_uid:str,
    ): 
        statement = select(BorrowBookModel).where(BorrowBookModel.uid == loan_uid)
        result =await session.exec(statement)
        return result.first()
        
    
    @staticmethod
    async def get_all_borrowed_history(
        session: AsyncSession,
        loan_status: LoanStatus
    ):
        
        statement =  select(BorrowBookModel).where(BorrowBookModel.loan_status ==  loan_status)
        borrowed_list = await session.exec(statement)
        return borrowed_list.all()
    
    
    @staticmethod
    async def get_user_borrowed_history(
        session: AsyncSession,
        loan_status: LoanStatus,
        user_uid = str,      
        
    ): 
        statement = select(BorrowBookModel).where(BorrowBookModel.loan_status == loan_status).where(BorrowBookModel.user_uid == user_uid).order_by(desc(BorrowBookModel.updated_at))
        borrowed_list = await session.exec(statement)
        return borrowed_list.all()
        
    
    @staticmethod 
    async def get_book_loan_history(
        session:AsyncSession,
        book_uid: str
    ): 
        statement = select(BorrowBookModel).where(BorrowBookModel.book_uid == book_uid).order_by(desc(BorrowBookModel.updated_at))
        result = await session.exec(statement)
        return result.all()
    