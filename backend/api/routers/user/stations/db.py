from core.base_db import Base

class StationInfoDb:
    """Низкоуровневый интерфейс базы данных для получения информации о станциях.
    
    Выполняет прямые SQL-запросы к таблице `info_station` с агрегацией данных.
    """
    def __init__(self, base_db: "Base"):
        self.db = base_db

    async def get_station(self, requested_id:int):
        """Получает агрегированные данные о станциях пользователя с группировкой по локациям.

        Запрос группирует станции по полю `location_name` и собирает их ID и ключи 
        в массивы PostgreSQL (ARRAY_AGG) со встроенной сортировкой по ключу.

        Args:
            requested_id: Идентификатор пользователя (user_id) для фильтрации станций.

        Returns:
            list[asyncpg.Record]: Список строк из БД. Каждая строка содержит поля:
                - 'label' (str): Название локации.
                - 'stations_count' (int): Количество станций в этой локации.
                - 'station_ids' (list[int]): Массив идентификаторов станций.
                - 'station_keys' (list[str]): Массив строковых ключей станций.
        """
        q = """
            SELECT 
                location_name as label,
                COUNT(*) as stations_count,
                ARRAY_AGG(id ORDER BY key) AS station_ids,
                ARRAY_AGG(key ORDER BY key) AS station_keys
            FROM info_station
            WHERE user_id = $1
            GROUP BY location_name
            ORDER BY location_name;          
            """
        async with self.db.pool.acquire() as conn:
            return await conn.fetch(q, requested_id)
        
