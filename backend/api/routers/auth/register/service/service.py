from backend.schemas.users import UserCreateRequest
from core.security.security import security
from core.base_db import Base
from backend.api.routers.auth.users import Users
from core.logger.logger import logger
from fastapi import HTTPException, status
import asyncpg


class RegistrationService:
    """
    Сервис регистрации пользователей.

    Отвечает за:
    - хеширование пароля;
    - создание пользователя в БД;
    - обработку ошибки дублирования email.

    В дальнейшем сюда добавляются:
    - проверка email-домена;
    - создание verification token;
    - отправка письма подтверждения.
    """
    def __init__(self, user_db: "Users"):
        self.db = user_db

    async def create(self, data: UserCreateRequest):
        """
        Создаёт нового пользователя.

        Args:
            data: Данные регистрации пользователя.

        Returns:
            dict: Идентификатор созданного пользователя и сообщение.

        Raises:
            HTTPException: Если пользователь с таким email уже существует.
        """
        hash_password = security.hashed_password(data.password.strip())
        try:
            user_id = await self.db.create_user(
                full_name=data.full_name,
                email=data.email,
                hash_password=hash_password,
                company=data.company,
                phone=data.phone,
                country=data.country
            )
           
        except asyncpg.exceptions.UniqueViolationError:
            logger.warning("USER ALREADY EXISTS")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email уже существует"
            )
        return {
                "user_id": user_id,
                "detail": "Пользователь создан"
            }