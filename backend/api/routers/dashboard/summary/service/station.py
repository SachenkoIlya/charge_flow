

from backend.api.routers.dashboard.summary.db import SummaryDB
from asyncpg import Record

class Station:
    def __init__(self, repository: "SummaryDB"):
            self.repository = repository

    @staticmethod
    def _normalize(row: Record) -> dict[str, int]:
        return   {
            'total_station': int(row['total_station']),
            'connected_stations': int(row['connected_stations'])
        }
    
    async def get_stations(self, user_id:int) -> dict[str, int]:
        """
        Нормализует статистику по станциям пользователя.
    
        Получает агрегированные данные из БД и приводит значения
        к стандартным Python-типам для последующей валидации
        через Pydantic и возврата в API.
    
        """
        row = await self.repository.get_connected_station(user_id)
        return self._normalize(row)