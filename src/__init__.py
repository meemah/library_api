from fastapi import FastAPI
from fastapi_utils.cbv import cbv

from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.user.user_routes import user_router

from .db.main import init_db
@asynccontextmanager
async def life_span(app:FastAPI):
    print(f"server is starting")
    await init_db()
    yield 
    print("server has ended")
    
app = FastAPI(
    lifespan=life_span
)



app.include_router(user_router,prefix="/users")
