from typing import Optional

from fastapi import Depends, APIRouter, Response, Form
from fastapi.responses import RedirectResponse
from backend.database.get_manager import get_manager
from core.logger.logger import make_logger
from core.security.security import security
from backend.database.manager import Manager
import os
from dotenv import load_dotenv
load_dotenv()

logger = make_logger(__name__, use_telegram=False)


router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/login')
async def check_login(
    response: Response,
    email: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    db_manager: Manager = Depends(get_manager),
    frontend_url = os.getenv('FRONTEND_URL')
    ):
    """
    Аутентификация пользователя (логин).
    Проверяет email и пароль пользователя. При успешной аутентификации
    генерирует JWT токен и сохраняет его в httpOnly cookie.
    Args:
        check_login (CheckLogin): Данные для входа:
            - email (str): Email пользователя
            - password (str): Пароль пользователя
        response (Response): Объект ответа FastAPI (используется для установки cookie)
        db_manager (Manager): Менеджер доступа к базе данных
    Returns:
        dict:
            При успешной аутентификации:
                {
                    "status": "ok"
                }
    Raises:
        HTTPException (401):
            Если пользователь не найден или пароль неверный:
                {
                    "detail": "Неверный email или пароль"
                }
    Side Effects:
        - Устанавливает cookie `access_token`:
            - httponly=True (недоступна из JS)
            - secure=True (только HTTPS)
            - samesite="lax"
    Notes:
        - Пароль проверяется через хеш (не сравнивается напрямую)
        - JWT токен содержит:
            - user_id
            - role
            - full_name
        - Cookie автоматически отправляется браузером в последующих запросах
    """
    if not email or not password:
        logger.debug(f"нет емаила или пароля")
        return RedirectResponse(
            url=f'{frontend_url}/login?error=missing_fields',
            status_code=302
        )
    if '@' not in email:
        return RedirectResponse(
            url=f'{frontend_url}/login?error=invalid_email',
            status_code=302
        )
    
    row = await db_manager.users.check_login(email)
    if not row:
        return RedirectResponse(
            url=f'{frontend_url}/login?error=invalid_credentials',
            status_code=302
        )
    verify = security.very_password(password, row['hash_password'])
    if not verify:
        return RedirectResponse(
            url=f'{frontend_url}/login?error=invalid_credentials',
            status_code=302
        )
    token = security.create_access_token(
        data={
            'full_name': row['full_name'],
            'user_id': row['id'],
            'role': row['role'] 
        }
    )
    redirect = RedirectResponse(
        url=f'{frontend_url}/summary',
        status_code=302
    )
    redirect.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,  #  True на проде
        samesite="lax"
    )
    return redirect
    