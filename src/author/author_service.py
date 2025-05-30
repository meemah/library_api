from sqlmodel.ext.asyncio.session import AsyncSession
from .author_schema import CreateAuthorSchema, UpdateAuthorSchema
from sqlmodel import select,desc    
from src.db.models import AuthorModel

class AuthorService:
    async def get_authors(
        self,
        session: AsyncSession,   
    ):
        statement = select(AuthorModel).order_by(desc(AuthorModel.updated_at))
        authors = await session.exec(statement)
        return authors.all()
    
    async def create_author(
        self,
        session: AsyncSession,
        author: CreateAuthorSchema
    ):
        new_author = AuthorModel(
            **author.model_dump()
        )
        session.add(new_author)
        await session.commit()
        await session.refresh(new_author)
        return new_author
        
    async def get_author(
        self,
        session:AsyncSession,
        author_id:str   
    ):
        statement = select(AuthorModel).filter(AuthorModel.uid == author_id)
        authors = await session.exec(statement)
        return authors.first()
    async def update_author(
        self,
        session: AsyncSession,
        author: UpdateAuthorSchema,
        id:str
    ):
        author_to_update = await self.get_author(session,id)
        
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
    
    async def delete_author(
        self,
        session:AsyncSession,
        id:str
    ):
        author = await self.get_author(session,id)
        if author is not None:
            await session.delete(author)
            await session.commit()
            return {}
        else: 
            return None
            
            
        
        
        
    