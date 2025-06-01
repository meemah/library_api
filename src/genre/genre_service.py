from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select,desc
from src.db.models import GenreModel
from .genre_schema import CreateGenreSchema,UpdateGenreSchema
class GenreService:
    
    @staticmethod
    async def get_genres(
        session:AsyncSession
    ):
        statement = select(GenreModel).order_by(desc(GenreModel.updated_at))
        genres = await  session.exec(statement)
        return genres.all()
    
    @staticmethod
    async def get_genre(
        session:AsyncSession,
        genre_id:str
    ):
        statement = select(GenreModel).filter(GenreModel.uid == genre_id)
        genres = await session.exec(statement)
        return genres.first()
    
    @staticmethod
    async def delete_genre(
        session:AsyncSession,
        genre_id:str
    ):
        genre = await GenreService.get_genre(session,genre_id)
        await session.delete(genre)
        await session.commit()
        if genre is not None:
            return {}
        else: 
            return None
    
    @staticmethod
    async def create_genre(
        session:AsyncSession,
        create_genre: CreateGenreSchema
    ):
        genre = GenreModel(
            **create_genre.model_dump()
        )
        session.add(genre)
        await session.commit()
        await session.refresh(genre)
        return genre
    
    @staticmethod
    async def update_genre(
        session:AsyncSession,
        genre_id:str,
        update_genre: UpdateGenreSchema
    ):
        genre = await GenreService.get_genre(session, genre_id)
        if genre is None:
            return None
        else:
            update_genre_dict = update_genre.model_dump()
            for k,v in update_genre_dict.items():
                if v is not None:
                    setattr(k,v,genre)
                    
            await session.commit()
            await session.refresh(genre)
            return genre
        