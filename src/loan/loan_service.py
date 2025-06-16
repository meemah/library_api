from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select,desc, update
from src.db.models import LoanBookModel, LoanStatus, LoanQueueModel, LoanQueueStatus
from src.book.book_service import BookService
from src.user.user_service import UserService
from src.utils.response.error import BookNotFound, UserNotFound, LoanedBookNotAvailable, UserLoanedBookAlready, LoanNotFound, BookNotOnLoan, UserOnQueue
from datetime import datetime
from typing import Optional

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
        has_exisitng_loan =await LoanService. user_active_loan(session, user.uid)
        if has_exisitng_loan:
            raise UserLoanedBookAlready()
        user_on_book_queue = await LoanService.user_on_book_queue(session, user.uid, book.uid)
        if user_on_book_queue:
            user_on_book_queue.queue_status = LoanQueueStatus.notified
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
                raise BookNotOnLoan()
            else:
                loan.return_date = datetime.now()
                loan.loan_status = LoanStatus.returned
                
                book = await BookService.get_book(session, loan.book_uid)
                if book is None:
                    raise BookNotFound()
                
                else: 
                    book.loaned_copies -=1
                    await LoanService.remove_all_user_from_book_queue(session,book.uid)
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
        loan_status: Optional[LoanStatus]
    ):
        
        statement =  select(LoanBookModel)
        if loan_status:
            statement = statement.where(LoanBookModel.loan_status ==  loan_status)
      
        borrowed_list = await session.exec(statement)
        return borrowed_list.all()
    
    
    @staticmethod
    async def get_user_loan_history(
        session: AsyncSession,
        loan_status: Optional[LoanStatus],
        user_uid = str,      
        
    ): 
        statement = select(LoanBookModel).where(LoanBookModel.user_uid == user_uid)

        if loan_status:
            statement = statement.where(LoanBookModel.loan_status == loan_status)

        statement = statement.order_by(desc(LoanBookModel.updated_at))

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
    
    @staticmethod
    async def add_book_to_queue(
        session:AsyncSession,
        user_email: str,
        book_uid:str
    ):
        book = await book_service.get_book(session, book_uid)
        if book is None:
            raise BookNotFound()
        user = await user_service.get_user(session, user_email)
        if user is None:
            return UserNotFound()
        has_exisitng_loan = await LoanService.user_active_loan(session, user.uid)
        if has_exisitng_loan:
            raise UserLoanedBookAlready()
        user_on_book_queue = await LoanService.user_on_book_queue(session, user.uid, book.uid)
        if user_on_book_queue:
            raise UserOnQueue()
        
        loan_queue = LoanQueueModel(
            user_uid= user.uid,
            user=user,
            book_uid=book.uid,
            book = book,
            
        )
        
        session.add(loan_queue)
        await session.commit()
        await session.refresh(loan_queue)
        return loan_queue
    
    @staticmethod
    async def notify_next_user_in_queue(
        session:AsyncSession,
        book_uid:str
    ):
        
        statement = select(LoanQueueModel).where(LoanQueueModel.book_uid == book_uid).order_by(LoanQueueModel.joined_at)
        result = await session.exec(statement)
        next_user = result.first()
        
        
        if next_user:
            next_user.queue_status = LoanQueueStatus.notified
            
            await session.commit()
            
            # send_email
            
    
    
    
    @staticmethod
    async def user_active_loan(
        session:AsyncSession,
        user_uid:str
    ):
        has_exisitng_loan = await LoanService.get_user_loan_history(
            session,
            LoanStatus.active,
            user_uid=user_uid
        )
        return has_exisitng_loan
    
    @staticmethod
    async def user_on_book_queue(
        session:AsyncSession,
        user_uid:str,
        book_uid:str
    ):
        statement = select(LoanQueueModel).where(
            LoanQueueModel.user_uid == user_uid , LoanQueueModel.book_uid == book_uid,
            LoanQueueModel.queue_status == LoanQueueStatus.waiting
        )
        loan_queues = await session.exec(statement)
        return loan_queues.first()
    
    @staticmethod
    async def remove_all_user_from_book_queue(
           session:AsyncSession,
        book_uid:str
    ):
        book = await BookService.get_book(
            session,book_uid
        )
        if book is None:
            raise BookNotFound()
        
        update_statement =  update(LoanQueueModel).where(
            LoanQueueModel.book_uid == book_uid,
            LoanQueueModel.queue_status == LoanQueueStatus.waiting
        ).values(
            queue_status = LoanQueueStatus.notified
        )
        
        await session.exec(update_statement)
        await session.commit()

        
        
        
        
        
        
