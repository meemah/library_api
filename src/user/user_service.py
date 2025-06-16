from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.db.models import UserModel
from src.user.schema import UserCreateSchema
from src.utils.password_util import generate_password_hash

from src.utils.redis import validate_otp
from src.utils.response.error import UserNotFound, OtpInvalid
class UserService:
    @staticmethod
    async def get_user(
        session: AsyncSession,
        email:str
    )-> UserModel | None:

        statement = select(UserModel).filter(UserModel.email == email)
        users = await session.exec(statement)
        return users.first()
    
    @staticmethod
    async def create_account(
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
    
    @staticmethod
    async def does_user_exist(
        session: AsyncSession,
        email:str
    )->bool:
        user = await UserService.get_user(session,email)
        return True if user is not None else False
    
    @staticmethod
    async def verify_user(
        session:AsyncSession,
        email:str,
        otp:str
    ):
        user = await UserService.get_user(session,email)
        if user is None:
            raise UserNotFound()
        else:
            otp_valid = await validate_otp(email,otp)
            if otp_valid is False:
                raise OtpInvalid()
            else:
                user.is_verified = True
                await session.commit()
                await session.refresh(user)
                return user