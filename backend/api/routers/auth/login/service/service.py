

from backend.api.routers.auth.users import Users
from fastapi.responses import RedirectResponse
from core.security.security import security
from core.security.settings import settings
from core.logger.logger import logger

class LoginService:
    """
    Сервис авторизации пользователя.

    Отвечает за:
    - проверку входных данных;
    - поиск пользователя по email;
    - проверку пароля;
    - создание JWT access token;
    - установку httpOnly cookie;
    - redirect после успешной или неуспешной авторизации.
    """

    def __init__(self, user_db: "Users"):
        self.db = user_db

    @staticmethod
    def _redirect_error(error: str) -> RedirectResponse:
        """Формирует HTTP-ответ для перенаправления пользователя на страницу входа с текстом ошибки.

        Используется во внешних интеграциях (например, OAuth2 или вебхуках), 
        когда вместо генерации JSON-ответа об ошибке нужно вернуть пользователя 
        в интерфейс фронтенда и показать ему уведомление.

        Args:
            error: Текст или код ошибки, который будет передан в URL.

        Returns:
            RedirectResponse: Объект ответа FastAPI с кодом 302 (Found) 
                для перенаправления браузера.
        """
        return RedirectResponse(
            url=f'{settings.FRONTEND_URL}/login?error={error}',
            status_code=302
            )
    
    async def authenticate(self, email:str, password: str) -> RedirectResponse:
        """
        Авторизует пользователя по email и паролю.
        Args:
            response:
                Объект ответа FastAPI.
            email:
                Email пользователя.
            password:
                Пароль пользователя.
        Returns:
            RedirectResponse:
                Redirect на frontend с результатом авторизации.
        """
        if not email or not password:
            logger.debug(f"нет емаила или пароля")
            return self._redirect_error('missing_fields')
        
        if '@' not in email:
            return self._redirect_error('invalid_email')
           
        row = await self.db.check_login(email)
        if not row:
            return self._redirect_error('invalid_credentials')
        
        verify = security.very_password(password, row['hash_password'])
        if not verify:
            return self._redirect_error('invalid_credentials')
        
        token = security.create_access_token(
            data={
                'full_name': row['full_name'],
                'user_id': row['id'],
                'role': row['role'] 
            }
        )
        redirect = RedirectResponse(
            url=f'{settings.FRONTEND_URL}/summary',
            status_code=302
        )
        redirect.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=True,  #  True на проде
            samesite="none",
            domain='.opower.su'
        )
        return redirect