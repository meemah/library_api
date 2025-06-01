from fastapi import APIRouter, Depends
from src.db.main import get_session
from src.utils.token_bearer import AccessToken
from sqlmodel.ext.asyncio.session import AsyncSession
from .author_service import AuthorService
from src.utils.response.success import SuccessResponse
from src.utils.response.error import AuthorNotFound
from src.db.models import AuthorModel
from .author_schema import CreateAuthorSchema, UpdateAuthorSchema
from typing import List
author_router = APIRouter()


@author_router.get("/",response_model= SuccessResponse[List[AuthorModel]])
async def get_authors(
    session: AsyncSession = Depends(get_session),
    _=Depends(AccessToken())
):
    authors = await AuthorService.get_authors(
        session
    )
    return SuccessResponse(
        message="Fetched authors",
        data = authors
    )

@author_router.get("/{author_id}",response_model=SuccessResponse[AuthorModel])
async def get_author(
    author_id:str,
    session: AsyncSession = Depends(get_session),
    _=Depends(AccessToken())
):
    author = await AuthorService.get_author(
        session,
        author_id
    )
    
    if (author is not None):
        return SuccessResponse(
            message="Fetched Author successfully",
            data = author
        )
    else: 
        raise AuthorNotFound()
    
@author_router.delete("/{author_id}",response_model=SuccessResponse)
async def delete_author(
    author_id:str,
    session: AsyncSession = Depends(get_session),
    _=Depends(AccessToken())
):
    author = await AuthorService.delete_author(session,author_id)
    
    if (author is not None):
        return SuccessResponse(
            message="Deleted Author successfully",
            data=None)
    else: 
        raise AuthorNotFound()

@author_router.post("/create", response_model=SuccessResponse[AuthorModel])
async def create_author(
    author: CreateAuthorSchema,
    session: AsyncSession = Depends(get_session),
    _=Depends(AccessToken())
):
    
    created_author = await AuthorService.create_author(
        session,
        author
    )
    
    return SuccessResponse(
        message="Author created successfully",
        data = created_author
    )

@author_router.put("/update/{author_id}")
async def update_author(
    author_id:str,
    author: UpdateAuthorSchema,
    session: AsyncSession = Depends(get_session),
    _=Depends(AccessToken())
):
    updated_author = await AuthorService.update_author(
        session,
        author,
        author_id    
    )
    
    if(updated_author is None):
        raise AuthorNotFound()
    else:
        return SuccessResponse(
            message="Author updated successfully",
            data = updated_author
        )
    
    