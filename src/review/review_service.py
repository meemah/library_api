from sqlmodel.ext.asyncio.session import AsyncSession
from src.book.book_service import BookService
from src.review.review_schema import CreateReviewSchema
from src.user.user_service import UserService

from src.db.models import ReviewModel
from sqlmodel import select
from typing import List
from src.utils.response.error import BookNotFound, UserNotFound

book_service = BookService()
user_service = UserService()

class ReviewService:
    
    @staticmethod
    async def get_book_reviews(
        session:AsyncSession,
        book_uid:str
    )->List[ReviewModel]:
 
        statement = select(ReviewModel).where(ReviewModel.book_uid == book_uid)
        reviews = await session.exec(statement)
        return reviews.all()
        
    
    @staticmethod
    async def add_book_review(
        session: AsyncSession,
        book_uid: str,
        create_review: CreateReviewSchema,
        email:str
    )->ReviewModel | None:
  
        book = await book_service.get_book(session,book_uid)
        
        if book is None:
            raise BookNotFound()
        
        user = await user_service.get_user(session,email)
        
        if user is None:
            raise UserNotFound()
        
        updated_review_with_user_book = ReviewModel(
            **create_review.model_dump(),
            user=user,
            book=book   
        )
        
        session.add(updated_review_with_user_book)
        await session.commit()
        await session.refresh()
        return updated_review_with_user_book
        
        
