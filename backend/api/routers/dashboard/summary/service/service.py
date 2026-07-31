from backend.api.routers.dashboard.summary.schemas.request import SummaryRequestModel
from core.base_db import Base
from backend.api.routers.dashboard.finance.service.conext import PeriodContext
from backend.api.routers.dashboard.summary.db import SummaryDB
from backend.api.routers.dashboard.summary.service.charts import Charts
from backend.api.routers.dashboard.summary.service.margin import Margin
from backend.api.routers.dashboard.summary.service.metrics import Metrics
from backend.api.routers.dashboard.summary.service.station import Station
from backend.api.routers.dashboard.summary.service.station_rating import StationRating
from backend.api.routers.dashboard.summary.service.utilisation import Utilisation

from backend.utils.gather_named import gather_named
from backend.utils.period_date import (
    get_last_30_days_with_comparable_period,
)




class SummaryService:
    """
    Сервис расчёта агрегированных метрик по зарядным сессиям.
    Использует SummaryDB для получения статистических данных и вычисления
    производных показателей эффективности использования зарядной инфраструктуры.
    """
    def __init__(self, base_db: "Base"):
        self.repository = SummaryDB(base_db)
        self.metrics = Metrics(self.repository)
        self.utilisation = Utilisation(self.repository)
        self.margin = Margin(self.repository)
        self.station = Station(self.repository)
        self.charts = Charts(self.repository)
        self.station_rating  = StationRating(self.repository)

    async def build_metrics(
        self, 
        ctx: PeriodContext,
        include_extended:bool=False
    ) -> dict:
        """
        Получает полный набор нормализованных метрик и агрегированных
        показателей для дашборда или аналитического отчёта.

        Метод параллельно выполняет сбор основных показателей, информации
        о подключённых зарядных станциях, коэффициента утилизации и
        финансовых метрик. При необходимости дополнительно формирует
        данные для построения графиков.

        Для повышения производительности все запросы выполняются
        асинхронно и обрабатываются одновременно.

        Args:
            user_id (int): Идентификатор пользователя.
            date_from (datetime): Начало анализируемого периода.
            date_to (datetime): Конец анализируемого периода.
            is_requested_metrics (bool, optional):
                Флаг необходимости получения данных для графиков.
                Если установлен в `True`, дополнительно возвращается
                блок с временными рядами метрик.

        Returns:
            dict:
                Словарь с агрегированными данными:

                - metrics — нормализованные бизнес-метрики;
                - station — информация о подключённых зарядных станциях;
                - utilisation — коэффициент утилизации зарядной инфраструктуры (%);
                - margin — показатели распределения выручки между партнёром и оператором;
                - charts — данные для построения графиков (если
                `is_requested_metrics=True`).

        Example:
            Возвращаемое значение:

            {
                "metrics": {...},
                "station": {...},
                "utilisation": 42.75,
                "margin": {
                    "partner_revenue": 7500.00,
                    "partner_pct": 75.0,
                    "operator_revenue": 2500.00,
                    "operator_pct": 25.0
                },
                "charts": {...}
            }
        Notes:
            Метод использует функцию `gather_named()` для параллельного
            выполнения всех асинхронных задач и объединения результатов
            в единый словарь.
        """
        tasks = {
            'metrics': self.metrics.get_metrics(ctx),
            'utilisation': self.utilisation.calc_utilisation(ctx),
            'margin': self.margin.get_margin_pct(ctx),
        }
        if include_extended:
            tasks['station'] = self.station.get_stations(ctx.user_id)
            tasks['charts'] = self.charts.get_metrics_chart(ctx)
            tasks['station_rating'] = self.station_rating.get_station_rating(ctx)
        return await gather_named(tasks)
    

    async def get_summary_with_comparison(
        self, 
        user_id:int, 
        payload: SummaryRequestModel,
    ) -> dict:
        """
        Формирует сводную аналитику за выбранный период и аналогичный
        предыдущий период для последующего сравнения.

        Метод рассчитывает границы сравниваемого периода той же
        продолжительности, получает набор ключевых метрик для обоих
        периодов и объединяет результаты в единую структуру.

        Для повышения производительности данные по текущему и
        сравнительному периодам запрашиваются параллельно.

        Args:
            user_id (int): Идентификатор пользователя.
            date_from (datetime): Начало анализируемого периода.
            date_to (datetime): Конец анализируемого периода.

        Returns:
            dict:
                Сводная информация, содержащая:

                - requested_metrics — метрики за выбранный период;
                - comparable_metrics — метрики за предыдущий сопоставимый период;
                - requested_period — границы выбранного периода;
                - comparable_period — границы периода сравнения.

        Notes:
            - Для выбранного периода дополнительно формируются данные
            для построения графиков.
            - Период сравнения имеет такую же продолжительность,
            как и анализируемый период.
            - Для параллельного выполнения запросов используется
            функция `gather_named()`.
        """

        date_range = get_last_30_days_with_comparable_period()
        date_from, date_to = date_range['requested']
        comparable_from, comparable_to = date_range['comparable']

        requested_ctx = PeriodContext(
            user_id=user_id,
            date_from=date_from,
            date_to=date_to,
            station_ids=payload.station_ids
            
        )
        comparable_ctx = PeriodContext(
            user_id=user_id,
            date_from=comparable_from,
            date_to=comparable_to,
            station_ids=payload.station_ids
        )

        data = await gather_named({
        'requested_metrics': self.build_metrics(
            ctx=requested_ctx,   
            include_extended=True
            ),
        'comparable_metrics': self.build_metrics(
            ctx=comparable_ctx  
            )
        })
        data['requested_period'] = {
            'date_from': date_from.strftime("%Y-%m-%d %H:%M:%S"),
            'date_to': date_to.strftime("%Y-%m-%d %H:%M:%S"),
        }
        data['comparable_period'] = {
            'date_from': comparable_from.strftime("%Y-%m-%d %H:%M:%S"),
            'date_to': comparable_to.strftime("%Y-%m-%d %H:%M:%S"),
        }
        return data