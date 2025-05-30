from fastapi.security import HTTPBearer
from fastapi import Request, Depends
from .token_util import decode_access_token
from .redis import jti_in_blocklist
from src.utils.response.error import InvalidToken, RevokedToken, AccessTokenRequired, RefreshTokenRequired
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.user.user_service import UserService


user_service = UserService()
class TokenBearer(HTTPBearer):
    def __init__(self, auto_error = True):
        super().__init__( auto_error=auto_error)
        
    async def __call__(self, request: Request):
        credential = await super().__call__(request)
        print(credential)
        token = credential.credentials
        try:
            token_data = decode_access_token(token)
        except Exception:
            raise InvalidToken()
        jti = token_data.get('jti')
        if not token_data:
            raise InvalidToken()
        if not jti:
            raise InvalidToken()
        if await jti_in_blocklist(jti):
            raise RevokedToken()
        self.verify_token_data(token_data)
        return token_data
            
    def verify_token_data(self, token_data):
        raise NotImplementedError("Please override in child token classes")
    

class AccessToken(TokenBearer):
    def verify_token_data(self, token_data):
        if token_data.get("refresh", False):
            raise AccessTokenRequired()
        


class RefreshToken(TokenBearer):
    def verify_token_data(self, token_data):
        if not token_data.get("refresh", False):
            raise RefreshTokenRequired()

async def get_user(
    session:AsyncSession= Depends(get_session),
    token=Depends(AccessToken())   
):
    user_email = token["user"]["email"]
    user = await user_service.get_user(session,user_email)
    return user
    