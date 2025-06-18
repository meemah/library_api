from sqlmodel.ext.asyncio.session import AsyncSession
from .author_schema import CreateAuthorSchema, UpdateAuthorSchema
from sqlmodel import select,desc    
from src.db.models import AuthorModel

class AuthorService:
    @staticmethod
    async def get_authors(
        session: AsyncSession,   
    )->list[AuthorModel]:
        """Retrieve all authors from the database, ordered by most recently updated.

        Args:
            session (AsyncSession): The database session used for the query.
            
        Returns:
            list[AuthorModel]: A list of AuthorModel instances sorted by updated_at descending.
        """        
        statement = select(AuthorModel).order_by(desc(AuthorModel.updated_at))
        authors = await session.exec(statement)
        return authors.all()
    
    @staticmethod
    async def create_author(
        session: AsyncSession,
        author: CreateAuthorSchema
    )-> AuthorModel:
        """Create an author

        Args:
            session (AsyncSession): The database session used for the query.
            author (CreateAuthorSchema): The data required to create the author.

        Returns:
            AuthorModel: The newly created author instance.
        """        
        new_author = AuthorModel(
            **author.model_dump()
        )
        session.add(new_author)
        await session.commit()
        await session.refresh(new_author)
        return new_author
        
    @staticmethod
    async def get_author(
        session:AsyncSession,
        author_uid:str   
    )->AuthorModel|None:
        """Retrieve an author based on the id from the database.

        Args:
            session (AsyncSession): The database session used for the query.
            author_id (str): the author's uid

        Returns:
            AuthorModel: The author instance by uid, or None if the author was not found.
        """        
        statement = select(AuthorModel).filter(AuthorModel.uid == author_uid)
        authors = await session.exec(statement)
        return authors.first()
    
    @staticmethod
    async def update_author(
        session: AsyncSession,
        author: UpdateAuthorSchema,
        uid:str
    )->AuthorModel| None:
        """Update an existing author's information.

        Args:
            session (AsyncSession): The database session used for the query.
            author (UpdateAuthorSchema): The updated data for the author.
            uid (str): The UID of the author to update.

        Returns:
            AuthorModel: The updated author instance, or None if the author was not found.
        """        
        
        author_to_update = await AuthorService.get_author(session,uid)
        
        if(author_to_update is None):
            return None
        else:
            updated_author_dict = author.model_dump()
            
            for k,v in updated_author_dict.items():
                if v is not None:
                    setattr(author_to_update, k,v)
            
            await session.commit()
            await session.refresh(author_to_update)
            return author_to_update
    
    @staticmethod
    async def delete_author(
        session:AsyncSession,
        uid:str
    ):
        """Delete an author from the database by ID.

        Args:
            session (AsyncSession):  The database session used for the query.
            uid (str): The UID of the author to delete.

        Returns:
            dict: An empty dictionary if deletion is successful.
            None: If the author with the given ID does not exist.
        """        
        author = await AuthorService.get_author(session,uid)
        if author is not None:
            await session.delete(author)
            await session.commit()
            return {}
        else: 
            return None
            
            
        
        
        
    