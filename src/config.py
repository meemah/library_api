
from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL:str
    JWT_SECRET:str
    JWT_ALGORITHM:str
    REDIS_URL:str
    MAIL_USERNAME:str
    MAIL_PASSWORD:str
    MAIL_SERVER:str
    MAIL_PORT:str
    MAIL_FROM:str
    MAIL_FROM_NAME:str
    DOMAIN:str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

Config = Settings()

broker_url = Config.REDIS_URL
result_backend = Config.REDIS_URL
broker_connection_retry_on_startup = True