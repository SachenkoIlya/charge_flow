from backend.api.routers.auth.register.schemas.response import UserCreateResponse
from backend.api.routers.auth.register.schemas.request import UserCreateRequest
from backend.manager.user import UserAuthManager
from backend.dependencies.get_manager import  get_user_create
from fastapi import APIRouter
from fastapi import Depends

ENDPOINT = '/register'
router = APIRouter(
    prefix="/v1/user/auth",
    tags=["user-auth"],
)

@router.post(
    ENDPOINT,
    response_model=UserCreateResponse,
    summary="Регистрация пользователя",
    description=(
        "Создаёт нового пользователя. "
        "Email должен быть уникальным, пароль сохраняется только в виде хеша."
    ),
)
async def register(
    data: UserCreateRequest,
    auth: UserAuthManager=Depends(get_user_create),
):
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
                    "error": [str(error)]
                
    Raises:
        - Пароль перед сохранением хешируется.
        - Email должен быть уникальным.
        - Ошибки логируются через logger.
    
    Регистрирует нового пользователя.

    Router отвеает только за приём HTTP-запроса,
    получение зависимостей и вызов сервисного слоя.
    """
    return await auth.registration.create(data=data)
       
    