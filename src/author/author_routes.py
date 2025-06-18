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
    """
    Retrieve a list of all authors.
    
    Args:
        session (AsyncSession, optional): The database session used to query authors. 
            Automatically injected by FastAPI.
        _ (_type_, optional):Access token dependency to enforce authentication. 
            Automatically injected by FastAPI.

    Returns:
        SuccessResponse[List[AuthorModel]]: A success response containing a list of author records.
    """    
    authors = await AuthorService.get_authors(
        session
    )
    return SuccessResponse(
        message="Fetched authors",
        data = authors
    )

@author_router.get("/{author_uid}",response_model=SuccessResponse[AuthorModel])
async def get_author(
    author_uid:str,
    session: AsyncSession = Depends(get_session),
    _=Depends(AccessToken())
):
    """Retrieve a specific author by their UID.

    Args:
        author_uid (str): The unique identifier (UUID) of the author to retrieve.
        session (AsyncSession, optional): The database session used to query authors. 
            Automatically injected by FastAPI.
        _ (_type_, optional):Access token dependency to enforce authentication. 
            Automatically injected by FastAPI.

    Raises:
        AuthorNotFound: If no author with the given UID is found in the database.

    Returns:
        SuccessResponse[AuthorModel]: A success response containing the author's information.
    """    
    
    author = await AuthorService.get_author(
        session,
        author_uid
    )
    
    if (author is not None):
        return SuccessResponse(
            message="Fetched Author successfully",
            data = author
        )
    else: 
        raise AuthorNotFound()
    
@author_router.delete("/{author_uid}",response_model=SuccessResponse)
async def delete_author(
    author_uid:str,
    session: AsyncSession = Depends(get_session),
    _=Depends(AccessToken())
):
    """Delete an author by their unique identifier (UID).

    Args:
        author_uid (str): The UUID of the author to be deleted.
        session (AsyncSession): The database session used to perform the deletion.
        _ (Any): Access token dependency to ensure the request is authenticated.

    Raises:
        AuthorNotFound: If the author with the given UID does not exist.

    Returns:
        SuccessResponse: A response indicating the author was successfully deleted.
    """    
    
    author = await AuthorService.delete_author(session,author_uid)
    
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
    """Create a new author.

    Args:
        author (CreateAuthorSchema): The data required to create the author.
        session (AsyncSession): The database session used to persist the author.
        _ (Any): Access token dependency to ensure the request is authenticated.

    Returns:
        SuccessResponse[AuthorModel]: A response object containing the newly created author.
    """    
    created_author = await AuthorService.create_author(
        session,
        author
    )
    
    return SuccessResponse(
        message="Author created successfully",
        data = created_author
    )

@author_router.put("/update/{author_uid}")
async def update_author(
    author_uid:str,
    author: UpdateAuthorSchema,
    session: AsyncSession = Depends(get_session),
    _=Depends(AccessToken())
):
    """Update an existing author by ID.

    Args:
        author_uid (str): The unique identifier of the author to update.
        author (UpdateAuthorSchema): The updated data for the author.
        session (AsyncSession, optional): The database session. Defaults to Depends(get_session).
        _ (Any, optional): Access token dependency. Defaults to Depends(AccessToken()).

    Raises:
        AuthorNotFound: Raised when the author with the given UID is not found.

    Returns:
       SuccessResponse[AuthorModel]: A response containing the updated author.
    """    
    updated_author = await AuthorService.update_author(
        session,
        author,
        author_uid    
    )
    
    if(updated_author is None):
        raise AuthorNotFound()
    else:
        return SuccessResponse(
            message="Author updated successfully",
            data = updated_author
        )
    
    