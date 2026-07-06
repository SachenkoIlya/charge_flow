from core.base_db import Base

class UserRepositoryDB:
    """Репозиторий для управления данными пользователей в базе данных.

    Предоставляет методы для выполнения SQL-запросов к таблице пользователей.

    Attributes:
        db (Base): Экземпляр базового класса для работы с подключениями к БД.
    """
    def __init__(self, base_db: "Base"):
        self.db = base_db

    
    async def get_company(self):
        """Получает список компаний всех пользователей с ролью 'investor'.

        Returns:
            list[asyncpg.Record]: Список строк из БД. Каждая строка содержит
                поля 'id' и 'company'.
        """
        q = """
            SELECT 
                id, company 
            FROM users_new
            WHERE role = 'investor'
            """
        async with self.db.pool.acquire() as conn:
            return await conn.fetch(q)