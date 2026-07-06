from core.base_db import Base
from asyncpg import Record

class ConnectOperatorDB:
    """Интерфейс базы данных для проверки и управления пользователями оператора.

    Предоставляет методы для работы с таблицей `users_new` с механизмами 
    отказоустойчивости при сетевых сбоях.

    Attributes:
        db (Base): Экземпляр базового класса для работы с пулом подключений БД.
    """
    def __init__(self, base_db: "Base"):
        self.db = base_db

    @Base.with_retries(
        retries=3, 
        delay=1.5, 
        msg_prefix='[ConnectOperator.check_user_existence]'
    )
    async def check_user_existence(self, email: str)-> Record | None:
        """Проверяет существование пользователя по его адресу электронной почты.

        Выполняет поиск в таблице `users_new` и возвращает базовые данные. 
        Благодаря декоратору `@with_retries`, при временных сбоях связи с БД 
        запрос будет автоматически повторен до 3 раз.

        Args:
            email: Электронная почта пользователя для проверки.

        Returns:
            Record | None: Объект записи asyncpg с полями 'id' и 'company', 
                или None, если пользователь с таким email не зарегистрирован.
        """
        q = """
            select id, company from users_new
            WHERE email = $1 
            """
        async with self.db.pool.acquire() as conn:
            return await conn.fetchrow(q, email)
        
        
    @Base.with_retries(
        retries=3, 
        delay=1.5, 
        msg_prefix='[ConnectOperator.check_first_run]'
    )
    async def check_first_run(self, user_id: str, run_mode: str, login: str) -> Record | None:
        """Проверяет статус запуска пайплайна для конкретного пользователя.

        Метод ищет запись в таблице `run_pipelines` по составному ключу 
        (пользователь, режим запуска и логин), чтобы определить текущее состояние.

        Args:
            user_id: Идентификатор пользователя в системе.
            run_mode: Режим запуска пайплайна (например, 'manual', 'scheduled').
            login: Логин учетной записи, из-под которой инициирован запуск.

        Returns:
            Record | None: Объект записи asyncpg, содержащий поле 'status', 
                или None, если такой запуск еще ни разу не производился.
        """
        q = """
            SELECT status FROM run_pipelines
            WHERE user_id = $1
                AND run_mode = $2
                AND login = $3
            """
        async with self.db.pool.acquire() as conn:
            return await conn.fetchrow(
               q,
               user_id,
               run_mode,
               login
            )
        


    @Base.with_retries(
        retries=3, 
        delay=1.5, 
        msg_prefix='[ConnectOperator.upsert_user_api_keys]'
    )
    async def upsert_user_api_keys(
        self, 
        user_id: int, 
        auth_type: str, 
        login: str, 
        password: str, 
        operator: str
    ):
        """Сохраняет или обновляет учетные данные оператора для пользователя (UPSERT).

        Если запись для данного `user_id` отсутствует, создается новая строка.
        Если запись уже существует (срабатывает ограничение уникальности `ON CONFLICT`),
        метод перезаписывает поля авторизации, логина, пароля и оператора новыми значениями.

        Args:
            user_id: Уникальный идентификатор пользователя.
            auth_type: Тип аутентификации (например, 'api_key', 'basic').
            login: Логин или идентификатор ключа для доступа к API.
            password: Пароль или секретная часть API-ключа.
            operator: Наименование оператора или интеграционной платформы.

        Returns:
            None
        """
        
        q = """
        INSERT INTO operator_credentials (
            user_id, auth_type, login, password, operator
        )
        VALUES ($1, $2, $3, $4, $5)
        ON CONFLICT (user_id) 
        DO UPDATE 
            SET auth_type = EXCLUDED.auth_type,
                login = EXCLUDED.login,
                password = EXCLUDED.password,
                operator = EXCLUDED.operator
            ;
        """
        async with self.db.pool.acquire() as conn:
            await conn.execute(
               q,
               user_id, 
               auth_type, 
               login, 
               password, 
               operator
            )