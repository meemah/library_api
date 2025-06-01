


from src.db.models import ReviewModel, UserModel
from typing import List
from src.utils.token_bearer import AccessToken, get_user
from src.db.main import get_session
from src.utils.response.success import SuccessResponse
from .review_service import ReviewService
from .review_schema import CreateReviewSchema
from fastapi import APIRouter, Depends


review_router = APIRouter()
review_service = ReviewService()



@review_router.get("\{book_uid}", response_model=List[ReviewModel])
async def get_book_reviews(
    book_uid: str,
    token = Depends(AccessToken()),
    session = Depends(get_session)
):
    reviews = await review_service.get_book_reviews(
        session, book_uid
    )
    return SuccessResponse(
        message = "Books Reviews Fetched",
        data = reviews
    )
    
@review_router.post("\{book_uid}", response_model=SuccessResponse[ReviewModel])
async def create_book_review(
    book_uid: str,
    create_review: CreateReviewSchema,
    user:UserModel = Depends(get_user),
    session = Depends(get_session),

):
    
    review = await review_service.add_book_review(
        session,
        book_uid,
        create_review,
        user.email
    )
    
    return SuccessResponse(
        message="Review Added",
        data = review
    )