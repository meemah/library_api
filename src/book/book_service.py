from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select,desc
from src.db.models import BookModel,AuthorModel, GenreModel
from src.book.book_schema import CreateBookSchema, UpdateBookSchema
import uuid
from typing import List
class  BookService:
    @staticmethod
    async def create_book(
        session:AsyncSession,
        create_book:CreateBookSchema
    ):
        book = BookModel(
            **create_book.model_dump(
                exclude={"authors", "genres"}
            )
        )
        session.add(book)
        await session.flush()
        if create_book.authors:
            author_uuids = [uuid.UUID(a) if isinstance(a, str) else a for a in create_book.authors]

            result = await session.exec(
                select(AuthorModel).where(AuthorModel.uid.in_(author_uuids))
            )
            authors = result.all()
            await session.refresh(book)
            book.authors.clear()
            book.authors.extend(authors)
        else:
            book.authors = []
        if create_book.genres:
            genres = await BookService.get_selected_genres(session, create_book.genres)
            book.genres = genres
        else: 
            book.genres = []
        
        await session.commit()
        await session.refresh(book)
        return book
    
    @staticmethod
    async def get_books(
        session:AsyncSession
    ): 
        statement = select(BookModel).order_by(BookModel.updated_at)
        books = await session.exec(statement)
        return books.all()
    
    @staticmethod
    async def get_book(
        session: AsyncSession,
        book_uid:str
    ):
        statement = select(BookModel).where(BookModel.uid == book_uid)
        books = await session.exec(statement)
        return books.first()
    
    @staticmethod 
    async def delete_book(
        session:AsyncSession,
        book_uid
    ):
        
        book = await BookService.get_book(session,book_uid)
        if book is None:
            return None
        else:
           await session.delete(book)
           await session.commit()
           return {}
    
    @staticmethod
    async def update_book(
        session: AsyncSession,
        book_uid:str,
        update_book_schema: UpdateBookSchema
        
    ):
        try:
            book = await BookService.get_book(session, book_uid)
            if book is None:
                print("Hellooo")
                return None
            else:
                update_book_dict = update_book_schema.model_dump(
                    exclude_unset=True, exclude={"authors", "genres"}
                )
                
                for k,v in update_book_dict.items():
                    if v is not None:
                        setattr(k,v, book)
                if update_book_schema.authors is not None:
                    selected_authors = await BookService.get_selected_authors(
                        session, update_book_schema.authors        
                    )
                    book.authors.clear()
                    book.authors.extend(selected_authors)
                if update_book_schema.genres is not None:
                    selected_genres = await BookService.get_selected_genres(
                        session,
                        update_book_schema.genres
                    )
                    book.genres.clear()
                    book.genres.extend(selected_genres)
            return book
                        
            
        except Exception as e:
            print("Exception {e}")
            # return None
        
        
        
    @staticmethod
    async def get_selected_authors(
        session:AsyncSession,
        uuids: List[uuid.UUID]
    )->List[GenreModel] :
        author_uuids = [uuid.UUID(a) if isinstance(a, str) else a for a in uuids]

        result = await session.exec(
                select(AuthorModel).where(AuthorModel.uid.in_(author_uuids))
            )
        authors = result.all()
        return authors
    
    
    @staticmethod
    async def get_selected_genres(
        session:AsyncSession,
        uuids: List[uuid.UUID]
    )-> List[GenreModel]:
        author_uuids = [uuid.UUID(a) if isinstance(a, str) else a for a in uuids]

        result = await session.exec(
                select(GenreModel).where(GenreModel.uid.in_(author_uuids))
            )
        authors = result.all()
        return authors