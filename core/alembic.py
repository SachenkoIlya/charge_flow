from core.security.settings import settings

def get_alembic_url() -> str:
    if settings.DB_HOST.startswith('/'):
        return (
            f"postgresql+asyncpg://"
            f"{settings.DB_USER}:{settings.DB_PASSWORD}"
            f"@/{settings.DB_NAME}"
            f"?host={settings.DB_HOST}"
        )

    return (
        f"postgresql+asyncpg://"
        f"{settings.DB_USER}:{settings.DB_PASSWORD}"
        f"@{settings.DB_HOST}:{settings.DB_PORT}"
        f"/{settings.DB_NAME}"
    )