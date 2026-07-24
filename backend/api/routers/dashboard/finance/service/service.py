from backend.api.routers.dashboard.finance.db import FinanceDB
from backend.api.routers.dashboard.finance.schemas import FinanceResponseModel
from backend.api.routers.dashboard.finance.service.charts.charts import  FinanceChartsService
from backend.api.routers.dashboard.finance.service.conext import PeriodContext
from backend.api.routers.dashboard.finance.service.normalize import FinanceMetricsService
from core.base_db import Base
from backend.core.gather_named import gather_named
from backend.core.period_date import get_date_range_from_period

class MetricFinance:
    """
    Сервис агрегации финансовых метрик пользователя.

    Выполняет сбор данных из различных источников (выручка, OPEX, CAPEX),
    рассчитывает финансовые показатели и формирует итоговый ответ
    для отображения в интерфейсе или API.

    Логика работы:
    1. Определяет диапазон дат на основе выбранного периода.
    2. Параллельно получает:
        - основные финансовые метрики;
        - операционные расходы (OPEX);
        - капитальные расходы (CAPEX).
    3. Объединяет результаты.
    4. Формирует итоговый набор финансовых показателей.

    Attributes:
        metrics_service (FinanceMetricsService):
            Сервис получения и подготовки финансовых данных.
    """
    def __init__(self, base_db: "Base"):
        self.fin_db = FinanceDB(base_db)
        self.metrics_service = FinanceMetricsService(self.fin_db)
        self.charts = FinanceChartsService(self.fin_db)
    
    async def get_metrics(
        self, 
        user_id: int, 
        period: str
    ) -> FinanceResponseModel:
        """
        Получить финансовые показатели пользователя за указанный период.
        Args:
            user_id (int):
                Идентификатор пользователя.

            period (str):
                Период выборки данных.
                Например: 'today', 'week', 'month', 'year'.
        Returns:
            dict:
                Подготовленный набор финансовых показателей, содержащий:
                    - выручку;
                    - OPEX;
                    - CAPEX;
                    - EBITDA;
                    - чистую прибыль;
                    - денежный поток;
                    - информацию о выбранном периоде.
        """
        date_from, date_to = get_date_range_from_period(period)

        ctx = PeriodContext(
            user_id=user_id,
            date_from=date_from,
            date_to=date_to
        )

        data = {
            'metrics': self.metrics_service.get_metrics(
                user_id=user_id,
                date_from=date_from,
                date_to=date_to
            ),
            'investment': self.metrics_service.get_investment_metrics(
                user_id=user_id,
                date_from=date_from,
                date_to=date_to,
            ),
            'charts': self.charts.build_charts(
                ctx=ctx
            ),
            'date_range': self.metrics_service.get_date_range(
                date_from=date_from,
                date_to=date_to,
                period=period,
                user_id=user_id,
            ),
        }

        result = await gather_named(data)
        return self.metrics_service.build_response(
            result=result,
        )
    
