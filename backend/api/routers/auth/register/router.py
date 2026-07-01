from backend.api.routers.auth.register.schemas import RegisterUserResponse
from backend.dependencies.get_manager import get_manager, get_user_create
from backend.schemas.users import UserCreateRequest
# from backend.database.manager import Manager
from backend.api.routers.auth.manager import UserAuthManager
from core.logger.logger import make_logger


from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
import asyncpg


logger = make_logger(__name__, use_telegram=False)

ENDPOINT = '/register'

router = APIRouter(
    prefix="/v1/user/auth",
    tags=["user-auth"],
)


@router.post(
    ENDPOINT,
    response_model=RegisterUserResponse,
    summary="Регистрация пользователя",
    description=(
        "Создаёт нового пользователя. "
        "Email должен быть уникальным, пароль сохраняется только в виде хеша."
    ),
)
async def register(
    data: UserCreateRequest,
    auth: UserAuthManager=Depends(get_user_create),
    # db_manager: Manager=Depends(get_manager)
):
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
    """
    Регистрирует нового пользователя.

    Router отвечает только за приём HTTP-запроса,
    получение зависимостей и вызов сервисного слоя.
    """
    return await auth.registration.create(data=data)
       
    