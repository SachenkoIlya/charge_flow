from backend.api.routers.dashboard.finance.db import FinanceDB
from backend.api.routers.dashboard.finance.schemas.response import FinanceResponseModel
from backend.api.routers.dashboard.finance.schemas.request import FinanceRequestModel
from backend.api.routers.dashboard.finance.service.charts.widget import  FinanceWidget
from backend.api.routers.dashboard.finance.service.conext import PeriodContext
from backend.api.routers.dashboard.finance.service.normalize import FinanceMetricsService
from core.base_db import Base
from backend.utils.gather_named import gather_named
from backend.utils.period_date import get_date_range_from_period
from datetime import datetime
from copy import deepcopy

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
        self.metrics = FinanceMetricsService(self.fin_db)
        self.widget = FinanceWidget(self.fin_db)

        self._handlers  = {
            'metrics': self.metrics.get_metrics,
            'investment': self.metrics.get_investment_metrics,
            'widgets': self.widget.build_sections,
            'date_range': self.metrics.get_date_range
        }

    def build_response(
            self,
            result: dict, 
            mask:str="%Y-%m-%d %H:%M:%S"
        ) -> dict:
            """
            Сформировать итоговый ответ с финансовыми метриками.
    
            Метод принимает результат параллельного выполнения запросов,
            добавляет информацию о периоде и рассчитывает производные показатели:
            OPEX, CAPEX, EBITDA, чистую прибыль и денежный поток.
    
            Args:
                result (dict):
                    Словарь с исходными данными:
                    - metrics: основные метрики;
                    - opex: операционные расходы;
                    - capex: капитальные расходы.
    
                period (str):
                    Название выбранного периода.
    
                date_from (datetime | None):
                    Начальная дата периода.
    
                date_to (datetime | None):
                    Конечная дата периода.
    
            Returns:
                dict:
                    Подготовленный ответ с финансовыми метриками и диапазоном дат.
            """
            prepare_result = deepcopy(result)
            date_range = prepare_result.get('date_range')
    
            date_from = date_range.get('date_from')
            date_to = date_range.get('date_to')
            
            date_from = datetime.strptime(date_from, mask) if date_from else None
            date_to = datetime.strptime(date_to, mask) if date_from else None

            financial_indicators, capex_total_amount = self.metrics.calculate_financial_indicators(prepare_result)
            payback_period = self.metrics.calculate_payback_period(
                net_profit=financial_indicators.get('net_profit'),
                capex_total_amount=capex_total_amount,
                date_from=date_from,
                date_to=date_to
            )
            prepare_result['metrics'].update({
                **financial_indicators,
                'payback_period': payback_period
            })
            return prepare_result

    async def get_metrics(
        self, 
        user_id: int, 
        payload: FinanceRequestModel
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
        date_from, date_to = get_date_range_from_period(payload.period)
        ctx = PeriodContext(
            user_id=user_id,
            date_from=date_from,
            date_to=date_to,
            period=payload.period,
            station_ids=payload.station_ids
        )
        tasks = {
            task: func(ctx)
            for task, func in self._handlers.items()
        }
        result = await gather_named(tasks)
        return self.build_response(
            result=result,
        )
    
