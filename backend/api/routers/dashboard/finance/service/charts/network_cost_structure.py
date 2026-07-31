

from backend.api.routers.dashboard.finance.db import FinanceDB
from datetime import datetime
from core.logger.logger import   logger
from backend.api.routers.dashboard.finance.service.conext import PeriodContext

class NetworkCostStructureCharts:
    def __init__(self, db: "FinanceDB"):
        self.db = db
        self.chart_name = 'network_cost_structure'
        
    async def get_data(
        self, 
        ctx: PeriodContext
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
            user_id=ctx.user_id,
            date_from=ctx.date_from,
            date_to=ctx.date_to,
            station_ids=ctx.station_ids
        )
        res = {
            k: float(v)
            for k, v in row.items()
        }

        return res
    