from backend.dependencies.get_manager import get_manager
from backend.schemas.users import UserCreate
from backend.database.manager import Manager

from core.logger.logger import make_logger
from core.security.security import security

from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
import asyncpg


logger = make_logger(__name__, use_telegram=False)

ENDPOINT = '/register'

router = APIRouter(
    prefix="/v1/user/auth",
    tags=["user"],
)


@router.post(ENDPOINT, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db_manager: Manager=Depends(get_manager)):
    # region DOC: register
    """
      Args:
        user (UserCreate): Данные пользователя для регистрации:
            - full_name (str): Полное имя
            - email (str): Email (должен быть уникальным)
            - password (str): Пароль (будет захеширован)
            - company (str, optional): Компания
            - phone (str, optional): Телефон
            - country (str, optional): Страна

        db_manager (Manager): Менеджер доступа к базе данных (Dependency Injection)

    Returns:
        dict:
            При успешной регистрации:
                {
                    "status": "success",
                    "user_id": int,
                    "error": []
                }

            Если пользователь уже существует:
                {
                    "status": "error",
                    "user_id": None,
                    "error": ["Email уже существует, Не удалось создать пользователя"]
                }

            При других ошибках:
                {
                    "status": "error",
                    "user_id": None,
                    "error": [str(error)]
                }

    Raises:
        asyncpg.exceptions.UniqueViolationError:
            Если пользователь с таким email уже существует.

    Notes:
        - Пароль перед сохранением хешируется.
        - Email должен быть уникальным.
        - Ошибки логируются через logger.
    
    """
    # endregion

    hash_password = security.hashed_password(user.password.strip())
    try:
        user_id = await db_manager.users.create_user(
            full_name=user.full_name,
            email=user.email,
            hash_password=hash_password,
            company=user.company,
            phone=user.phone,
            country=user.country
        )
        return {
            "user_id": user_id,
            "detail": "Пользователь создан"
        }
    except asyncpg.exceptions.UniqueViolationError:
        logger.warning("USER ALREADY EXISTS")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email уже существует"
        )
       
    