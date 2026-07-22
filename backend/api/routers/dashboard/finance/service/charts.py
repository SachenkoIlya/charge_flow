from backend.api.routers.dashboard.finance.db import FinanceDB
from core.base_db import Base
from datetime import datetime
from core.logger.logger import logger
from asyncpg import Record

class FinanceChartsService:
    """
    Сервис подготовки данных для финансовых графиков и диаграмм.

    Отвечает за получение агрегированных данных из БД и преобразование
    их в формат, удобный для отображения на дашборде.

    Основные задачи:
    - подготовка структуры операционных расходов (OPEX);
    - агрегация данных для круговых и столбчатых диаграмм;
    - формирование единого формата ответа для UI.

    Attributes:
        db (FinanceDB):
            Слой доступа к финансовым данным.
    """
    def __init__(self, base_db: "Base"):
        self.db = FinanceDB(base_db)
        self.chart_name: str = 'network_cost_structure'

    @staticmethod
    def demical_to_float(data:Record) -> dict:
        return  {
            k: float(v) 
            for k, v in data.items()
        }
    

    async def get_cost_structure(
        self, 
        user_id: int, 
        date_from:datetime=None, 
        date_to:datetime=None
    ):
        """
        Получить данные для диаграммы структуры затрат.

        Является публичной точкой входа для формирования графика
        распределения операционных расходов.

        Args:
            user_id (int):
                Идентификатор пользователя.

            date_from (datetime | None):
                Начальная дата периода.

            date_to (datetime | None):
                Конечная дата периода.

        Returns:
            dict:
                Структура данных для отображения диаграммы затрат.
        """

        row = await self.db.get_full_network_cost_structure(
            user_id=user_id,
            date_from=date_from,
            date_to=date_to
        )

        return {
            self.chart_name: self.demical_to_float(row)
        }