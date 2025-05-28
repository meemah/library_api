from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel,create_engine
from ..config import Config
from typing import AsyncGenerator
import ssl

ssl_context = ssl.create_default_context()
engine = AsyncEngine(
    create_engine(
        url=Config.DATABASE_URL,
        echo=True,
         connect_args={"ssl": ssl_context},
    )
)
session_maker = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession

)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session()->AsyncGenerator[AsyncSession, None]:
    async with session_maker() as sesion:
        yield sesion

