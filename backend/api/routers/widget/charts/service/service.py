from backend.api.routers.widget.charts.db import ChartsDB
from backend.api.routers.widget.charts.service.chart_registry import CHART_REGISTRY 
from core.base_db import Base


class ChartService:
    def __init__(self, base_db: "Base"):
        self.chart_db = ChartsDB(base_db)
    

    async def resolve_charts(self, user_id: int, payload):
        ...

