from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select,desc
from src.db.models import LoanBookModel, LoanStatus
from src.book.book_service import BookService
from src.user.user_service import UserService
from src.utils.response.error import BookNotFound, UserNotFound, LoanedBookNotAvailable, UserLoanedBookAlready, LoanNotFound, BookNotOnLoan
from datetime import datetime

book_service = BookService()
user_service = UserService()

class LoanService:
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
        
        if total_copies <=0 or total_copies == book.loaned_copies:
            raise LoanedBookNotAvailable()
        has_exisitng_loan = await LoanService.get_user_loan_history (
            session,
            LoanStatus.active,
            user_uid=user.uid
        )
        if has_exisitng_loan:
            raise UserLoanedBookAlready()
        book.loaned_copies += 1
        
        borrowed = LoanBookModel(
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
        
        loan =  await LoanService.get_loan_details(session, loan_uid)
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
                    book.loaned_copies -=1
                    await session.commit()
                    await session.refresh(loan)
                    return loan
            
        
        
    @staticmethod 
    async def  get_loan_details(
        session:AsyncSession, 
        loan_uid:str,
    ): 
        statement = select(LoanBookModel).where(LoanBookModel.uid == loan_uid)
        result =await session.exec(statement)
        return result.first()
        
    
    @staticmethod
    async def get_all_loan_history(
        session: AsyncSession,
        loan_status: LoanStatus
    ):
        
        statement =  select(LoanBookModel).where(LoanBookModel.loan_status ==  loan_status)
        borrowed_list = await session.exec(statement)
        return borrowed_list.all()
    
    
    @staticmethod
    async def get_user_loan_history(
        session: AsyncSession,
        loan_status: LoanStatus,
        user_uid = str,      
        
    ): 
        statement = select(LoanBookModel).where(LoanBookModel.loan_status == loan_status).where(LoanBookModel.user_uid == user_uid).order_by(desc(LoanBookModel.updated_at))
        borrowed_list = await session.exec(statement)
        return borrowed_list.all()
        
    
    @staticmethod 
    async def get_book_loan_history(
        session:AsyncSession,
        book_uid: str
    ): 
        statement = select(LoanBookModel).where(LoanBookModel.book_uid == book_uid).order_by(desc(LoanBookModel.updated_at))
        result = await session.exec(statement)
        return result.all()
    