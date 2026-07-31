from backend.legacy.stats.service.metrics import MetricStats
from backend.api.routers.admin.companies.service.metrics import UserRepositoryMetrics
from core.base_db import Base


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