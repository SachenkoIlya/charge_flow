from backend.api.routers.admin.companies.service.metrics import UserRepositoryMetrics
from backend.api.routers.dashboard.finance.service.metrics import MetricFinance
from backend.api.routers.user.stations.service.metrics import StationInfo
from backend.api.routers.dashboard.stats.service.metrics import MetricStats
from backend.api.routers.dashboard.summary.service.metrics import MetricSummary
from backend.api.routers.investments.investments_and_expenses.services.data import InvestmentsAndExpensesRepository
from backend.api.routers.admin.system.services.data import SystemReposytory
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
        self.summary = MetricSummary(base_db)
        self.finance = MetricFinance(base_db)
        
class ManagerMetrics:
    def __init__(self, base_db: "Base"):
        self.stats = MetricStats(base_db)
        self.user_reposytory = UserRepositoryMetrics(base_db)

class ManagerFinance:
    def __init__(self, base_db: "Base"):
        self.investments_and_expenses = InvestmentsAndExpensesRepository(base_db)
        self.station_info = StationInfo(base_db)



class ManagerSystem:
    def __init__(self, base_db: "Base"):
        self.monitoring  = SystemReposytory(base_db)