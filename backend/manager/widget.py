from backend.api.routers.widget.charts.service.service import ChartService
from backend.api.routers.widget.tables.service.service import TableService
from core.base_db import Base


    


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