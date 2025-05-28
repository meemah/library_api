import redis.asyncio as redis
from src.config import Config

JTI_EXPIRY = 3600

token_blocklist = redis.Redis.from_url(
    url=Config.REDIS_URL
)

async def add_jti_to_blocklist(jti:str):
    await token_blocklist.set(
        name=jti,value="revoke",ex=JTI_EXPIRY
    )
    
async def jti_in_blocklist(jti:str)->bool:
    return True if await token_blocklist.get(jti) is not None else False