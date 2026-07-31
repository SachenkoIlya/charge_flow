from backend.api.routers.admin.system.services.data import SystemReposytory
from core.base_db import Base

class ManagerSystem:
    def __init__(self, base_db: "Base"):
        self._monitoring  = SystemReposytory(base_db)
    @property
    def monitoring(self):
        return self._monitoring
    