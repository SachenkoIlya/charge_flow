from core.security.security import security
from core.base_db import Base
from fastapi import HTTPException, status
from backend.api.routers.auth.connect_operator.db import ConnectOperatorDB
from backend.schemas.connect_operator import ConnectOperator
from core.base_db import Base
from asyncpg import Record

class ConnectOperatorService:
    """
    Сервис подключения оператора к пользователю.

    Отвечает за:
    - проверку существования пользователя;
    - определение типа авторизации оператора;
    - шифрование credentials;
    - сохранение access данных оператора.
    """
    def __init__(self, base_db: "Base"):
        self.db = ConnectOperatorDB(base_db)

    @staticmethod
    def resolve_auth_type(operator: str) -> str:
        """
        Определяет тип авторизации оператора.
        Для оператора `volt` используется bearer-auth,
        для остальных операторов — basic-auth.
        """
        return 'basic' if operator != 'volt' else 'bearer'
       
    async def upsert(self, user_data: Record, data: ConnectOperator):
        """
        Создаёт или обновляет учётные данные оператора.

        Выполняет:

        - определение типа авторизации;
        - шифрование логина и пароля;
        - сохранение API-учётных данных пользователя.

        Args:
            user_data (Record):
                Запись пользователя, полученная из базы данных.

                Используется идентификатор пользователя (`id`)
                для привязки учётных данных оператора.

            data (ConnectOperator):
                Данные подключения оператора.

        Returns:
            dict:
                Результат успешного подключения.

                Пример:

                {
                    "detail": "Оператор подключен"
                }
        """
        user_id = user_data['id']
        auth_type = self.resolve_auth_type(data.operator)
        # шифруем парооли 
        encrypt_password = security.encrypt_data(data.password)
        encrypt_login = security.encrypt_data(data.login)
        # добавляем пользователя
        await self.db.upsert_user_api_keys(
            user_id=user_id,
            auth_type=auth_type,
            login=encrypt_login,
            password=encrypt_password,
            operator=data.operator
        )
        return {
            "detail": "Оператор подключен"
        }
    
    async def connect(self, data: ConnectOperator) -> dict:
        """
        Подключает оператора к пользователю.

        Выполняет поиск пользователя по email.
        Если пользователь существует, создаёт или обновляет
        его учётные данные для выбранного оператора.

        Args:
            data (ConnectOperator):
                Данные подключения оператора.

                Содержат:

                - email пользователя;
                - название оператора;
                - логин оператора;
                - пароль оператора.

        Returns:
            dict:
                Результат успешного подключения.

                Пример:

                {
                    "detail": "Оператор подключен"
                }

        Raises:
            HTTPException:
                Если пользователь с указанным email
                не зарегистрирован в системе.
        """
        user_data = await self.db.check_user_existence(email=data.email)
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Инвестор не зарегестрирован'
            )
        return await self.upser(user_data=user_data, data=data)
        
       