from typing import Optional

from fastapi import Depends, APIRouter, Response, Form
from fastapi.responses import RedirectResponse
from backend.manager.user import UserAuthManager
from backend.dependencies.get_manager import get_user_create


ENDPOINT = "/login"
router = APIRouter(
    prefix="/v1/user/auth",
    tags=["user-auth"],
)


@router.post(
    ENDPOINT,
    response_class=RedirectResponse,
    summary="Авторизация пользователя",
    description="Проверяет email и пароль, создаёт JWT и сохраняет его в httpOnly cookie.",
)
async def check_login(
    response: Response,
    email: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    auth: UserAuthManager=Depends(get_user_create),
):
    """
    Выполняет авторизацию пользователя.

    Router отвечает только за получение HTTP-запроса
    и передачу данных в сервисный слой.

    Вся бизнес-логика находится в
    `LoginService.authenticate()`.
    """
   
    return await auth.login.authenticate(email, password)
    