from fastapi import FastAPI
from fastapi_utils.cbv import cbv
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.user.user_routes import user_router
from .db.main import init_db
from src.utils.response.error import register_all_errors
from src.author.author_routes import author_router
from src.genre.genre_routes import genre_router
from src.book.book_routes import book_router
from src.loan.loan_routes import loan_router
from src.review.review_routes import review_router
@asynccontextmanager
async def life_span(app:FastAPI):
    print(f"server is starting")
    await init_db()
    yield 
    print("server has ended")
    
app = FastAPI(
    lifespan=life_span
)
register_all_errors(app)


app.include_router(user_router,prefix="/users",tags=["Users"])
app.include_router(author_router,prefix="/authors",tags=["Authors"])
app.include_router(genre_router,prefix="/genres",tags=["Genres"])
app.include_router(book_router,prefix="/books",tags=["Books"])
app.include_router(loan_router,prefix="/loans",tags=["Loans"])
app.include_router(review_router,prefix="/reviews",tags=["Reviews"])