from backend.api.routers.admin.companies.service.metrics import UserRepositoryMetrics
from core.base_db import Base


class ManagerMetrics:
    def __init__(self, base_db: "Base"):
        self._user_repository = UserRepositoryMetrics(base_db)
    @property
    def user_repository(self):
        return self._user_repository