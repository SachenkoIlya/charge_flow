from ..utils.logger.logger import make_logger
import asyncpg
import os
import asyncio
logger = make_logger(__name__, use_telegram=False)

class Base:
    
    # region DOC: BaseDB class
    """
    BaseDB — базовый класс для работы с PostgreSQL через asyncpg.

    Назначение:
    -----------
    Обеспечивает единообразное подключение к базе данных, открытие пула
    соединений, повторные попытки при ошибках и автоматическое закрытие
    соединений. Используется как фундамент для всех других DB-классов,
    которые выполняют конкретные SQL-запросы.

    Основные задачи класса:
    -----------------------
    1. Формирование DSN-подключения на основе .env.
    2. Управление пулом соединений (create_pool / close).
    3. Предоставление контекстного менеджера (async with BaseDB()).
    4. Универсальный декоратор @with_retries для повторных попыток запросов.
    5. Надёжный механизм повторов при временных ошибках базы данных.
    6. Логирование успешных подключений и ошибок.

    Используется в проекте как:
    ---------------------------
        class BotDB(BaseDB):
            ... объединяет под-DB классы

        db = BotDB()
        await db.connect()

    Почему BaseDB выделен в отдельный класс:
    ----------------------------------------
    - Централизует подключение к БД.
    - Исключает дублирование одинаковой логики.
    - Обеспечивает единый пул соединений для всех DB-классов.
    - Упрощает тестирование и масштабирование проекта.
    - Позволяет изолировать низкоуровневую логику PostgreSQL.

    Атрибуты:
    ---------
    dsn : str
        Строка подключения PostgreSQL в формате:
        postgresql://user:password@host:port/dbname

    pool : asyncpg.Pool | None
        Пул соединений PostgreSQL, создаваемый через asyncpg.create_pool().

    Методы:
    -------
    @staticmethod with_retries
        Декоратор, который повторяет выполнение функции при ошибках.
        Используется для connect(), close() и может применяться в потомках.

    connect()
        Создаёт пул соединений. Переподключается, если предыдущий был закрыт.

    close()
        Корректно закрывает пул соединений.

    __aenter__ / __aexit__
        Обеспечивают возможность использования через "async with BaseDB()"

    Пример использования:
    ---------------------
        db = BotDB()
        await db.connect()

        client_id = await db.clients.add_client(...)
        stores = await db.stores.get_stores()

    Пример через контекстный менеджер:
    ----------------------------------
        async with BotDB() as db:
            client = await db.clients.get_client(123)

    Механика декоратора with_retries:
    ---------------------------------
    - Выполняет функцию до N раз (default = 5).
    - Между попытками растущая задержка (delay * attempt).
    - Логирует ошибки и финальное исключение.
    - Позволяет ботам работать стабильно при временных проблемах БД.

    Особенности реализации:
    -----------------------
    - Пул соединений создаётся только один раз.
    - При pool._closed создаётся новый пул (горячее переподключение).
    - Безопасное закрытие через close().
    - Поддержка .env для конфигурации.
    - Логгер интегрирован в каждое действие.

    Кому использовать BaseDB:
    -------------------------
    - BotDB — главный DB-класс Telegram-бота.
    - CoreDB — для серверной части проекта (если есть).
    - Любым другим сервисам, которым нужен единый подход
      к подключению к PostgreSQL.

    Главная цель:
    -------------
    Сбалансировать надёжность, чистоту архитектуры и удобство использования
    в средних и крупных проектах.
    """
    # endregion
    
    TRANSIENT_ERRORS = (
            asyncpg.exceptions.PostgresConnectionError,
            asyncpg.exceptions.CannotConnectNowError,
            asyncpg.exceptions.TooManyConnectionsError,
            TimeoutError,
            ConnectionError,
            asyncio.TimeoutError,
            # EndpointConnectionError,
            # ConnectionClosedError,
            # ReadTimeoutError,
        )
    
    def __init__(self, dsn:str = None):
        self.dsn = dsn or (
            f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
            f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        )
        self.pool: asyncpg.Pool | None = None



    
    
    @staticmethod
    def _row_to_dict(row):
        if isinstance(row, list):
            if not row:
                return []
            if hasattr(row[0], 'keys'):
                return [dict(r) for r in row]
            return row
        if hasattr(row, 'keys'):
            return dict(row)
        if isinstance(row, tuple):
            if len(row) > 0 and hasattr(row[0], 'keys'):
                return [dict(r) for r in row]
            return {'value': row[0]}
        
        logger.warning(f"[DB:_row_to_dict] Unexpected row type: {type(row)}")
        return None
    
    
    @staticmethod
    def with_retries(retries=5, delay=1.5, msg_prefix:str=None):
        def decorator(func):
            async def wrapper(*args, **kwargs):
                
                for attempt in range(1, retries + 1):
                    try:
                        logger.warning(
                            f"{msg_prefix or ''} 🔁 Попытка {attempt}/{retries}")
                        
                        res =  await func(*args, **kwargs)
                        
                        logger.info(f"{msg_prefix or ''} ✅ Успех на попытке {attempt}")
                        return res
                    
                    except Base.TRANSIENT_ERRORS as e:
                        
                        if attempt < retries:
                            wait_time = delay * attempt
                            
                            logger.warning(
                                f"{msg_prefix or ''} ⚠️ Ошибка ({type(e).__name__}): {e}. "
                                f"Будет повтор через {wait_time:.1f}с (попытка {attempt}/{retries})"
                            )
                            
                            await asyncio.sleep(wait_time)
                        else:
                            logger.exception(
                                f"{msg_prefix or ''} ❌ ФАТАЛЬНАЯ ошибка ({type(e).__name__}): {e}. "
                                f"Попытка {attempt}/{retries} — прекращаю выполнение"
                            )
                            raise

                    except Exception as e:
                        logger.exception(
                            f"{msg_prefix or ''} 💥 НЕ RETRY ошибка ({type(e).__name__}): {e}"
                        )
                    raise
                
            return wrapper
        return decorator
    

    
    @with_retries(retries=5, delay=1.5)
    async def connect(self):
        # region DOC: connect
        """
        Создаёт пул соединений с PostgreSQL, если он отсутствует или закрыт.
        Использует asyncpg.create_pool().

        Особенности:
        - Автоматический повтор подключения (декоратор with_retries).
        - Логирует успешный коннект.
        """
        # endregion
        
        if not self.pool or self.pool._closed:
            self.pool = await asyncpg.create_pool(dsn=self.dsn)
            logger.info("📡 Подключение к БД установлено")




    @with_retries(retries=5, delay=1.5)
    async def close(self):
        # region DOC: close
        """
        Корректно закрывает пул соединений, если он существует и не закрыт.

        Особенности:
        - Защищено повторными попытками (with_retries).
        - Логирует завершение соединения.
        """
        # endregion
        
        if self.pool and not self.pool._closed:
            await self.pool.close()
            logger.info("🔌 Соединение с БД закрыто")
    
    

    async def __aenter__(self):
        # region DOC: __aenter__
        """
        Автоматически подключает БД при входе в 'async with'.
        Возвращает объект DB (self).
        """
        # endregion

        await self.connect()
        return self



    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # region DOC: __aexit__
        """
        Автоматически закрывает пул при выходе из 'async with'.
        Исключения не подавляет.
        """
        # endregion
        await self.close()


    
    async def acquire_export_lock(self, conn, run_id: str) -> bool:
        row = await conn.fetchrow(
            "SELECT pg_try_advisory_lock(hashtext($1)) AS locked",
            run_id
        )
        return row["locked"]
    
    async def release_export_lock(self, conn, run_id: str):
        await conn.execute(
            "SELECT pg_advisory_unlock(hashtext($1))",
            run_id
        )