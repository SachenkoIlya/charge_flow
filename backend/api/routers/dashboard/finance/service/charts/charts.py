from backend.api.routers.dashboard.finance.db import FinanceDB
from datetime import datetime
from backend.api.routers.dashboard.finance.service.charts.accumulated_cash_flow import CashFlowHistory
from backend.api.routers.dashboard.finance.service.charts.network_cost_structure import NetworkCostStructureCharts
from backend.api.routers.dashboard.finance.service.conext import PeriodContext
from backend.core.gather_named import gather_named
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
    def __init__(self, db: "FinanceDB"):
        self.network_cost_structure = NetworkCostStructureCharts(db)
        self.cash_flow_history = CashFlowHistory(db)

    @staticmethod
    def demical_to_float(data:Record) -> dict:
        return  {
            k: float(v) 
            for k, v in data.items()
        }

    async def build_charts(
        self,
        ctx: PeriodContext
    ):
        data = {
            self.network_cost_structure.chart_name: self.network_cost_structure.get_data(ctx),
            self.cash_flow_history.chart_name: self.cash_flow_history.get_data(ctx)
        }

# accumulated_cash_flow
        return await gather_named(data)
    