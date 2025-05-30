from fastapi import APIRouter,Depends
from src.utils.response.success import SuccessResponse
from src.utils.response.error import GenreNotFound
from src.db.main import get_session
from src.utils.token_bearer import AccessToken
from .genre_service import GenreService
from src.db.models import GenreModel
from typing import List
from .genre_schema import CreateGenreSchema, UpdateGenreSchema

genre_router = APIRouter()
genre_service = GenreService()

@genre_router.get("/",response_model=SuccessResponse[List[GenreModel]])
async def get_genres(
    session=Depends(get_session),
    _ = Depends(AccessToken())    
):
    genres = await genre_service.get_genres(
        session
    )
    
    return SuccessResponse(
        message="Genres fetched",
        data=genres
    )
    
@genre_router.get("/{genre_id}",response_model=SuccessResponse[GenreModel])
async def get_genres(
    genre_id:str,
    session=Depends(get_session),
    _ = Depends(AccessToken())    
):
    genre = await genre_service.get_genre(
        session,genre_id
    )
    if genre is  None:
        raise GenreNotFound()
    
    return SuccessResponse(
        message="Genre fetched",
        data=genre
    )

@genre_router.delete("/{genre_id}",response_model=SuccessResponse)
async def get_genres(
    genre_id:str,
    session=Depends(get_session),
    _ = Depends(AccessToken())    
):
    genre = await genre_service.delete_genre(
        session,genre_id
    )
    if genre is None:
        raise GenreNotFound()
    
    return SuccessResponse(
        message="Genre deleted",
        data=None
    )


@genre_router.put("/update/{genre_id}",response_model=SuccessResponse[GenreModel])
async def get_genres(
    genre_id:str,
   update_genre: UpdateGenreSchema,
    session=Depends(get_session),
   
    _ = Depends(AccessToken())    
):
    genre = await genre_service.update_genre(
        session,genre_id,update_genre
    )
    if genre is None:
        raise GenreNotFound()
    
    return SuccessResponse(
        message="Genre updated",
        data=None
    )
    
@genre_router.post("/create",response_model=SuccessResponse[GenreModel])
async def create_genre(
   create_genre: CreateGenreSchema,
    session=Depends(get_session),
   
    _ = Depends(AccessToken())    
):
    genre = await genre_service.create_genre(
        session,create_genre
    )
    if genre is None:
        raise GenreNotFound()
    
    return SuccessResponse(
        message="Genre created",
        data=genre
    )






