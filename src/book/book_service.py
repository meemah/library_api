from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select,desc
from src.db.models import BookModel,AuthorModel, GenreModel,AuthorBookLink,GenreBookLink
from src.book.book_schema import CreateBookSchema, UpdateBookSchema
import uuid
from typing import List, Optional
from sqlalchemy.orm import selectinload
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
        session:AsyncSession,
        author_uid: Optional[str],
        genre_uid: Optional[str]
    ): 
        statement = select(BookModel)
        filters = []
        eager_options = []
        if author_uid:
            statement = statement.join(AuthorBookLink, AuthorBookLink.book_uid == BookModel.uid).join(AuthorModel, AuthorModel.uid == AuthorBookLink.author_uid)
            filters.append(AuthorModel.uid == author_uid)
            eager_options.append(selectinload(BookModel.authors))
        

        if genre_uid: 
            statement =statement.join(GenreBookLink, GenreBookLink.book_uid == BookModel.uid).join(GenreModel, GenreModel.uid ==GenreBookLink.genre_uid)
            filters.append(GenreModel.uid == genre_uid)
            eager_options.append(selectinload(BookModel.genres))
            
        if eager_options:
            statement = statement.options(*eager_options)
        
        if filters:
            statement = statement.where(*filters)

        statement = statement.order_by(BookModel.updated_at)
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
           await session. delete(book)
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
                return None
            else:
                update_book_dict = update_book_schema.model_dump(
                    exclude_unset=True, exclude={"authors", "genres","reviews","loans"}
                )
                
                for k,v in update_book_dict.items():
                    if v is not None:
                        setattr(book,k,v, )
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
            print(str(e))
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