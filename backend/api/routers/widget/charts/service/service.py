from backend.api.routers.widget.charts.core.base import BaseService
from backend.api.routers.widget.charts.db import ChartsDB
from backend.api.routers.widget.charts.schemas import ChartsRequestSchema
from backend.api.routers.widget.charts.service.chart_registry import CHART_REGISTRY 
from core.logger.logger import logger
from backend.core.gather_named import gather_named  
import asyncio
from typing import Any

class ChartService(BaseService):
    """Сервисный слой для сборки и обработки аналитических графиков (компонентов дашборда).

    Использует паттерн 'Фабрика/Реестр' (Registry Pattern) для динамического 
    управления процессорами графиков. При инициализации класс кэширует экземпляры 
    всех зарегистрированных обработчиков, обеспечивая их изоляцию и переиспользование.

    Attributes:
        registry (dict[str, Any]): Глобальный реестр процессоров графиков (`CHART_REGISTRY`).
        mode (str): Идентификатор сервиса, жестко задан как `'charts'`.
        chart_db (ChartsDB): Слой работы с базой данных для аналитических запросов.
        handlers (dict[str, Any]): Реестр инициализированных объектов-обработчиков 
            (Handlers) для каждого типа графика.
    """
    registry: dict[str, Any] = CHART_REGISTRY
    mode: str = 'charts'

    def __init__(self, base_db):
        """Инициализирует сервис графиков, оборачивая базовую БД в ChartsDB."""
        super().__init__(ChartsDB(base_db))
    
    @property
    def chart_db(self) -> ChartsDB:
        """ChartsDB: Возвращает специализированный слой БД для графиков."""
        return self.db
    
    async def execute(
        self, 
        user_id:int, 
        payload: ChartsRequestSchema
    ) -> dict:
            """Запускает процесс построения или обработки графика.

            Args:
                user_id (int): Идентификатор пользователя, запрашивающего данные.
                payload (ChartsRequestSchema): Валидированные параметры запроса графика.

            Returns:
                dict: Результат обработки графика, готовый для отдачи клиенту.
            """
            return await self._execute(
                user_id=user_id,
                payload=payload
            )

