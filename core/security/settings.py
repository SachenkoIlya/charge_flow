from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: str = "dev"

    FRONTEND_HOST: str
    FRONTEND_PORT: int
    FRONTEND_URL: str
    SECRET_KEY_FROM_UI: str

    BACKEND_HOST: str
    BACKEND_PORT: int
    BACKEND_URL: str
    
    JWT_SECRET: str
    ALGORITHM: str = "HS256"
    
    ENCRYPTION_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int

    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_BUCKET: str
    S3_ENDPOINT: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()