
from backend.api.routers.auth.login.service.service import LoginService
from core.base_db import Base
from backend.api.routers.auth.register.service.service import RegistrationService
from backend.api.routers.auth.connect_operator.service.service import ConnectOperatorService
from backend.api.routers.auth.users import Users


class UserAuthManager:
    """
    Менеджер сервисов аутентификации пользователя.

    Предоставляет единую точку доступа ко всем сервисам,
    связанным с регистрацией, авторизацией и управлением
    учётными данными пользователя.

    Attributes:
        registration (RegistrationService):
            Сервис регистрации новых пользователей.

        connect_operator (ConnectOperatorService):
            Сервис подключения операторов зарядных сетей.
    """

    def __init__(self, db: "Base"):
        """
        Инициализирует менеджер сервисов аутентификации.

        Args:
            db (Base):
                Экземпляр подключения к базе данных.
        """
        self.user_db = Users(db)
        self.registration = RegistrationService(self.user_db)
        self.login = LoginService(self.user_db)
        self.connect_operator = ConnectOperatorService(db)
        