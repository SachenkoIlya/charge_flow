from core.base_db import Base
from backend.api.routers.user.stations.db import StationInfoDb


class StationInfo:
    """Бизнес-логика и нормализация данных для информации о станциях.

    Выступает в качестве сервисного слоя, который запрашивает агрегированные 
    данные из БД и приводит их к формату, ожидаемому схемой API (`StationSchemas`).

    Attributes:
        db (StationInfoDb): Экземпляр репозитория для выполнения запросов к БД.
    """
    def __init__(self, base_db: "Base"):
        self.db = StationInfoDb(base_db)

    async def get_stations(self, requested_id: int):
        """Получает и нормализует сгруппированные данные о станциях пользователя.

        Args:
            requested_id: Идентификатор пользователя (user_id), для которого 
                запрашиваются станции.

        Returns:
            list[dict]: Список нормализованных словарей с данными о группах станций.
        """
        return await self.normalize_data(requested_id)

    async def normalize_data(self, requested_id: int) -> list[dict]:
        """Преобразует сырые строки из базы данных в формат ответа API.

        Извлекает записи через репозиторий и формирует валидную структуру 
        ключей, полностью соответствующую Pydantic-модели `StationSchemas`.

        Args:
            requested_id: Идентификатор пользователя для фильтрации в БД.

        Returns:
            list[dict]: Массив словарей, где каждый элемент содержит ключи 
                'label', 'stations_count', 'station_ids' и 'station_keys'.
        """

        # Запрашиваем сырые данные (строки/записи asyncpg.Record) из БД
        res = await self.db.get_station(requested_id)
        
        # Маппим полученные поля в список словарей для последующей валидации в FastAPI
        return [
            {
                'label': r['label'],
                'stations_count': r['stations_count'],
                'station_ids': r['station_ids'],
                'station_keys': r['station_keys']
            
            }
            for r in res
        ]