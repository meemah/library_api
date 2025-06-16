

from fastapi import APIRouter,Depends, Query
from src.utils.response.success import SuccessResponse
from src.utils.response.error import BookNotFound
from src.db.main import get_session
from src.utils.token_bearer import AccessToken
from .book_service import BookService
from src.db.models import BookModel
from typing import List
from .book_schema import CreateBookSchema, GetBookSchema, UpdateBookSchema


book_router = APIRouter()


@book_router.post("/create", response_model=SuccessResponse[BookModel])
async def create_book(
    create_book:CreateBookSchema,
    session = Depends(get_session),
    _ = Depends(AccessToken())
):
    book = await  BookService.create_book(session,create_book)
    return SuccessResponse(
        message = "Book created successfully",
        data = book
    )

@book_router.get("/", response_model=SuccessResponse[List[BookModel]])
async def get_books(
       session = Depends(get_session),
       author = Query(default=None),
       genre = Query(default = None),
    _ = Depends(AccessToken()) 
):
    books = await BookService.get_books(session,author_uid=author,genre_uid=genre)
    
    return SuccessResponse(
        message= "Books Fetched",
        data = books
    )

@book_router.get("/{book_uid}", response_model=SuccessResponse[GetBookSchema])
async def get_book(
    book_uid:str,
    session = Depends(get_session),
        _ = Depends(AccessToken()) 
):
    book = await BookService.get_book( session, book_uid )
    if book is None:
        raise BookNotFound()
    else:
        return SuccessResponse(
            message= "Book Fetched",
            data = book
        )

@book_router.delete("/{book_uid}",response_model=SuccessResponse)
async def delete_book(
    book_uid:str,
    session = Depends(get_session),
        _ = Depends(AccessToken()) 
    
):
    is_deleted = True if await BookService.delete_book(session,book_uid) is not None else False
    if is_deleted:
        return SuccessResponse(
            message = "Deleted Successfully",
            data = None
        )
    else: 
        raise BookNotFound()

@book_router.put("/{book_uid}",response_model=SuccessResponse[BookModel])
async def update_book(
    book_uid:str,
    update_book_schema: UpdateBookSchema,
    session = Depends(get_session),
        _ = Depends(AccessToken())  
):
    book = await BookService.update_book(session, book_uid,update_book_schema)
    if book is not None:
        return SuccessResponse(
            message = "Updated Successfully",
            data = book
        )
    else: 
        raise BookNotFound()

    