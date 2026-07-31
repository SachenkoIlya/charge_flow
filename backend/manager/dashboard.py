from core.base_db import Base
from backend.api.routers.dashboard.summary.service.service import SummaryService
from backend.api.routers.dashboard.finance.service.service import MetricFinance


class ManagerDashboardMetrics:
    """
    Фасад сервисов аналитики дашборда руководителя.

    Объединяет сервисы получения сводных показателей и финансовой
    аналитики, предоставляя единую точку доступа к данным дашборда.

    Используется для формирования ключевых метрик, финансовых
    показателей, инвестиционной аналитики и данных для визуализации.

    Состав сервиса:
        - SummaryService:
            Сводные показатели по станциям, зарядным сессиям и выручке.

        - MetricFinance:
            Финансовые метрики, инвестиционные показатели и данные
            для построения графиков.

    Attributes:
        summary (SummaryService):
            Сервис сводной аналитики дашборда.

        finance (MetricFinance):
            Сервис финансовой аналитики и визуализации данных.
    """
    def __init__(self, base_db: "Base"):
        self._summary = SummaryService(base_db)
        self._finance = MetricFinance(base_db)
    @property
    def summary(self):
        return self._summary
    @property
    def finance(self):
        return self._finance