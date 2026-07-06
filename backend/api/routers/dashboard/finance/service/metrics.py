from backend.api.routers.dashboard.finance.service.charts import FinanceChartsService
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
        self.metrics_service = FinanceMetricsService(base_db)
        # self.charts = FinanceChartsService(base_db)
    
    async def get_metrics(self, user_id: int, period: str):
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
        data = {
            'metrics': self.metrics_service.get_metrics(
                user_id=user_id,
                date_from=date_from,
                date_to=date_to
            ),
            'investment': self.metrics_service.get_investment_metrics_v2(
                user_id=user_id,
                date_from=date_from,
                date_to=date_to,
            ),
            # 'charts': self.charts.get_cost_structure(
            #     user_id=user_id,
            #     date_from=date_from,
            #     date_to=date_to,
            # )
        }

        result = await gather_named(data)
        return self.metrics_service.build_response(
            result=result,
            period=period,
            date_from=date_from,
            date_to=date_to,
        )
    
