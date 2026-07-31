from backend.api.routers.admin.companies.db import UserRepositoryDB
from backend.legacy.stats.db import StatsDB
from core.base_db import Base


class MetricsStats:
    
    def __init__(self, base_db: "Base"):
        self.stats = StatsDB(base_db)
       



class  UserRepositoryMetrics:
    """Бизнес-логика и нормализация данных для репозитория пользователей.

    Служит прослойкой между сырыми данными из БД и эндпоинтами, 
    приводя структуры данных к нужному для API формату.

    Attributes:
        db (UserRepositoryDB): Экземпляр репозитория для прямых запросов к БД.
    """
    def __init__(self,  base_db: "Base"):
        self.db = UserRepositoryDB(base_db)

    async def get_companies(self):
        """Получает и нормализует список компаний инвесторов.

        Returns:
            list[dict]: Список словарей, готовых для валидации в Pydantic.
        """
        return await self.normalize_company_data()
    
    
    async def normalize_company_data(self):
        """Трансформирует сырые строки из БД в формат для API.

        Переименовывает поле 'company' в 'name' для соответствия схеме ответа.

        Returns:
            list[dict]: Массив словарей со структурой {'id': int, 'name': str}.
        """
        rows = await self.db.get_company()
        return [
            {
                'id': r['id'],
                'name': r['company']
            }
            for r in rows
        ]
    
    