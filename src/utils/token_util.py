
from src.config import Config
from src.user.schema import UserSchema
import jwt
import uuid
from datetime import datetime,timedelta

from passlib.context import CryptContext

ACCESS_TOKEN_EXPIRY = timedelta(
    seconds=3600)


def create_access_token(user:UserSchema, refresh=False, expiry: timedelta = None ):
    payload = {}
    payload["user"]=user.model_dump()
    payload['exp'] = datetime.now() + (expiry if expiry is not None else ACCESS_TOKEN_EXPIRY)
    payload["jti"] = str(uuid.uuid4())
    payload['refresh'] = refresh
    return jwt.encode(
        payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM
    )

def decode_access_token(token:str)-> dict | None:
    try:
        return jwt.decode(jwt=token,key=Config.JWT_SECRET,algorithms=Config.JWT_ALGORITHM)
    except jwt.PyJWKError as e:
        return None