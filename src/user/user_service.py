from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.db.models import UserModel
from src.user.schema import UserCreateSchema
from src.utils.password_util import generate_password_hash
class UserService:
    async def get_user(
        self,
        session: AsyncSession,
        email:str
    )-> UserModel | None:

        statement = select(UserModel).filter(UserModel.email == email)
        users = await session.exec(statement)
        return users.first()
    
    async def create_account(
        self,
        session:AsyncSession,
        user_create_schema: UserCreateSchema
    )->UserModel:
        user = UserModel(
            **user_create_schema.model_dump()
        )
        user.password = generate_password_hash(user_create_schema.password)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    
    async def does_user_exist(
        self,
        session: AsyncSession,
        email:str
    )->bool:
        user = await self.get_user(session,email)
        return True if user is not None else False