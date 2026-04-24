from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os
load_dotenv()


class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv('JWT_SECRET')
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 90
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # class Config:
    #     env_file = ".env"


settings = Settings()