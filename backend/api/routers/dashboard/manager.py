from backend.api.routers.admin.companies.service.metrics import UserRepositoryMetrics
from backend.api.routers.dashboard.finance.service.metrics import MetricFinance
from backend.api.routers.user.stations.service.metrics import StationInfo
from backend.api.routers.dashboard.stats.service.metrics import MetricStats
from backend.api.routers.dashboard.summary.service.metrics import MetricSummary
from backend.api.routers.investments.investments_and_expenses.services.data import InvestmentsAndExpensesRepository
from backend.api.routers.admin.system.services.data import SystemReposytory
from backend.api.routers.widget.charts.service.service import ChartService
from backend.api.routers.widget.tables.service.service import TableService
from core.base_db import Base


class ManagerDashboardMetrics:
    """
    Фасад сервисов аналитики дашборда руководителя.

    Объединяет сервисы получения сводных показателей и финансовой
    аналитики, предоставляя единую точку доступа к данным дашборда.

    Используется для формирования ключевых метрик, финансовых
    показателей, инвестиционной аналитики и данных для визуализации.

    Состав сервиса:
        - MetricSummary:
            Сводные показатели по станциям, зарядным сессиям и выручке.

        - MetricFinance:
            Финансовые метрики, инвестиционные показатели и данные
            для построения графиков.

    Attributes:
        summary (MetricSummary):
            Сервис сводной аналитики дашборда.

        finance (MetricFinance):
            Сервис финансовой аналитики и визуализации данных.
    """
    def __init__(self, base_db: "Base"):
        self._summary = MetricSummary(base_db)
        self._finance = MetricFinance(base_db)
    @property
    def summary(self):
        return self._summary
    @property
    def finance(self):
        return self._finance
    
class ManagerMetrics:
    def __init__(self, base_db: "Base"):
        self._stats = MetricStats(base_db)
        self._user_repository = UserRepositoryMetrics(base_db)
    @property
    def investments(self):
        return self._stats
    @property
    def user_repository(self):
        return self._user_repository

class ManagerFinance:
    def __init__(self, base_db: "Base"):
        self._investments_and_expenses = InvestmentsAndExpensesRepository(base_db)
        self._station_info = StationInfo(base_db)
    @property
    def investments(self):
        return self._investments_and_expenses
    @property
    def station_info(self):
        return self._station_info
    

class ManagerSystem:
    def __init__(self, base_db: "Base"):
        self._monitoring  = SystemReposytory(base_db)
    @property
    def monitoring(self):
        return self._monitoring
    
class ManagerWidget:
    def __init__(self, base_db: "Base"):
        self._charts  = ChartService(base_db)
        self._tables = TableService(base_db)
    @property
    def charts(self):
        return self._charts
    @property
    def tables(self):
        return self._tables