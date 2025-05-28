from fastapi.security import HTTPBearer
from fastapi import Request
from .token_util import decode_access_token
from .redis import jti_in_blocklist

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
            print("Invalid Token")
            # raise InvalidToken
        jti = token_data.get('jti')
        if not token_data:
            print("Invalid")
        if not jti:
            print("Invalid")
        if await jti_in_blocklist(jti):
            print("Revoked")
        self.verify_token_data(token_data)
        return token_data
            
    def verify_token_data(self, token_data):
        raise NotImplementedError("Please override in child token classes")
    

class AccessToken(TokenBearer):
    def verify_token_data(self, token_data):
        if token_data.get("refresh", False):
            print("Access required")
        


class RefreshToken(TokenBearer):
    def verify_token_data(self, token_data):
        if not token_data.get("refresh", False):
            print("Refresh required")