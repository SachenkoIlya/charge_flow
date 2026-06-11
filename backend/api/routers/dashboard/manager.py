from backend.api.routers.dashboard.companies.service.metrics import UserRepositoryMetrics
from backend.api.routers.dashboard.station.service.metrics import StationInfo
from backend.api.routers.dashboard.stats.service.metrics import MetricStats
from backend.api.routers.dashboard.summary.service.metrics import MetricSummary
from backend.api.routers.investments.investments_and_expenses.services.data import InvestmentsAndExpensesRepository
from backend.api.routers.system.services.data import SystemReposytory
from core.base_db import Base


class ManagerDashboardMetrics:
    def __init__(self, base_db: "Base"):
        self.summary = MetricSummary(base_db)
        
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