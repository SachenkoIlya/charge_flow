from backend.api.routers.dashboard.companies.service.metrics import UserRepositoryMetrics
from backend.api.routers.dashboard.station.service.metrics import StationInfo
from backend.api.routers.dashboard.stats.service.metrics import MetricStats
from core.base_db import Base



class ManagerMetrics:
    def __init__(self, base_db: "Base"):
        self.stats = MetricStats(base_db)
        self.user_reposytory = UserRepositoryMetrics(base_db)
        self.station_info = StationInfo(base_db)