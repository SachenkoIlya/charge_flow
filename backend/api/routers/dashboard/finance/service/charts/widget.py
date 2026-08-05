from backend.api.routers.dashboard.finance.db import FinanceDB
from backend.api.routers.dashboard.finance.service.charts.accumulated_cash_flow import CashFlowHistory
from backend.api.routers.dashboard.finance.service.charts.network_cost_structure import NetworkCostStructure
from backend.api.routers.dashboard.finance.service.charts.station_financials import StationFinancials
from backend.api.routers.dashboard.finance.service.conext import PeriodContext
from backend.utils.gather_named import gather_named
from core.logger.logger import logger
from asyncpg import Record


class FinanceWidget:
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
        # self.network_cost_structure = NetworkCostStructure(db)
        # self.cash_flow_history = CashFlowHistory(db)
        self.station_financials = StationFinancials(db)
        self.tasks = [
            # self.network_cost_structure, 
            # self.cash_flow_history, 
            self.station_financials
        ]

    @staticmethod
    def demical_to_float(data:Record) -> dict:
        return  {
            k: float(v) 
            for k, v in data.items()
        }

    async def build_sections(
        self,
        ctx: PeriodContext
    ):
        data = {
            service.chart_name: service.get_data(ctx)
            for service in self.tasks
        }
        return await gather_named(data)
    