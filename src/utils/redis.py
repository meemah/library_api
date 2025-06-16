import redis.asyncio as redis
from src.config import Config

JTI_EXPIRY = 3600
OTP_EXPIRY = 600

redis_client = redis.Redis.from_url(
    url=Config.REDIS_URL
)

async def add_jti_to_blocklist(jti:str):
    await redis_client.set(
        name=f"jti:{jti}",value="revoke",ex=JTI_EXPIRY
    )
    
async def jti_in_blocklist(jti:str)->bool:
    return True if await redis_client.get(jti) is not None else False


async def create_otp(email:str, otp:str,ttl: int = OTP_EXPIRY):
   await redis_client.set(
       name=f"otp:{email}",
       value=otp,
       ex=ttl
   )
async def validate_otp(
    email:str,
    otp:str
):
    key = f"otp:{email}"
    value = await redis_client.get(key)
    print(f"hellooo {value}")
    if value:
        await redis_client.delete(key)
        return True
    else:
        return False