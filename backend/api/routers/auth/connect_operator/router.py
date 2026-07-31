from backend.api.routers.auth.connect_operator.schemas.response import OperatorConnectResponse
from backend.api.routers.auth.connect_operator.schemas.request import ConnectOperatorRequest

from backend.dependencies.get_manager import get_user_create
from backend.dependencies.admin_required import admin_required
from fastapi import APIRouter
from fastapi import Depends

from backend.manager.user import UserAuthManager



ENDPOINT = "/connect"   
router = APIRouter(
    prefix="/v1/user/auth/operators",
    tags=["user-auth"],
)


@router.post(
    ENDPOINT,
    response_model=OperatorConnectResponse,
    summary="Подключение оператора",
    description=(
        "Подключает оператора зарядной сети к пользователю. "
        "Доступно только пользователю с ролью admin."
    ),
)
async def connect(
    data: ConnectOperatorRequest, 
    _: None = Depends(admin_required),
    auth: UserAuthManager=Depends(get_user_create)
):
    """
    Подключает оператора зарядной сети.

    Router отвечает за:

    - получение HTTP-запроса;
    - проверку роли пользователя;
    - вызов сервиса подключения оператора.

    Бизнес-логика подключения оператора находится в
    `auth.connect_operator.connect()`.
    """
    return await auth.connect_operator.connect(data=data)
    
    