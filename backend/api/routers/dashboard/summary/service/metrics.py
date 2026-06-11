from backend.api.routers.dashboard.summary.db import SummaryDB
from core.logger.logger import logger
from backend.api.routers.dashboard.summary.schemas import SummaryResponseModel
from backend.api.routers.dashboard.summary.service.charts import _normalize_metrics_chart
from backend.core.gather_named import gather_named
from backend.core.period_date import (
    get_period_days,
    comparable_period,
    get_date_expr,
    _calc_utilisation
)
from core.base_db import Base
from datetime import datetime


class MetricSummary:
    """
    Сервис расчёта агрегированных метрик по зарядным сессиям.
    Использует SummaryDB для получения статистических данных и вычисления
    производных показателей эффективности использования зарядной инфраструктуры.
    """
    def __init__(self, base_db: "Base"):
        self.db = SummaryDB(base_db)

    async def calc_utilisation(self, user_id, date_from:datetime, date_to:datetime):
        """
        Рассчитывает коэффициент утилизации (Utilisation Rate) зарядных станций
        за указанный период.
        Утилизация показывает, какой процент доступного времени зарядные
        станции фактически использовались для зарядки.
        Формула расчёта:
            utilisation = charging_minutes /
                          (evse_count * period_minutes) * 100
        где:
            - charging_minutes — суммарное время зарядки за период в минутах;
            - evse_count — количество доступных EVSE;
            - period_minutes — длительность периода в минутах.
        Args:
            user_id: Идентификатор пользователя.
            date_from (datetime): Начало периода расчёта.
            date_to (datetime): Конец периода расчёта.
        Returns:
            float:
                Процент утилизации зарядной инфраструктуры,
                округлённый до двух знаков после запятой.
                Возвращает 0, если количество доступных минут равно нулю.
        Example:
            Для периода в 24 часа (1440 минут),
            2 зарядных точек и 720 минут зарядки:
                available_minutes = 2 * 1440 = 2880
                utilisation = 720 / 2880 * 100 = 25.0
            Результат:
                25.0
        """
       
        rows = await self.db.get_utilisation_metrics(user_id, date_from, date_to)
        return _calc_utilisation(
            charging_minutes=float(rows['charging_minutes']),
            evse_count=float(rows['evse_count']),
            date_from=date_from,
            date_to=date_to
        )
    
    async def get_margin_pct(self,  user_id: int, date_from: datetime, date_to:datetime):
        """
        Рассчитывает распределение выручки между партнёром и оператором
        за указанный период.
        На основании агрегированных финансовых показателей вычисляет:
        - доход партнёра (`partner_revenue`);
        - долю дохода партнёра в общей выручке (`partner_pct`);
        - доход оператора (валовую маржу, `operator_revenue`);
        - долю дохода оператора в общей выручке (`operator_pct`).
        Процентные значения рассчитываются относительно общей выручки.
        Если общая выручка отсутствует или равна нулю, проценты принимают
        значение `0`.
        
        Args:
            user_id (int): Идентификатор пользователя.
            date_from (datetime): Начало периода расчёта.
            date_to (datetime): Конец периода расчёта.

        Returns:
            dict:
                Словарь с финансовыми показателями:
                - partner_revenue (float) — доход партнёра;
                - partner_pct (float) — доля дохода партнёра в общей выручке, %;
                - operator_revenue (float) — доход оператора (валовая маржа);
                - operator_pct (float) — доля дохода оператора в общей выручке, %.
                Все значения округляются до двух знаков после запятой.
        
        Example:
            Возвращаемое значение:
            {
                "partner_revenue": 7500.00,
                "partner_pct": 75.0,
                "operator_revenue": 2500.00,
                "operator_pct": 25.0
            }
        """
        rows = await self.db.get_margin_metrics(user_id, date_from, date_to)
        partner_revenue = float(rows['partner_revenue'])
        total_revenue = float(rows['total_revenue'])
        gross_margin = float(rows['gross_margin'])
        margin_pct = (
            partner_revenue / total_revenue * 100 
            if total_revenue > 0
            else 0
        )
        operator_pct = (
            gross_margin / total_revenue * 100
            if total_revenue > 0
            else 0
        )
        return {
            'partner_revenue': round(partner_revenue, 2),
            'partner_pct': round(margin_pct, 2),
            'operator_revenue': round(gross_margin, 2),
            'operator_pct': round(operator_pct, 2)
        }
    
    async def normalize_metrics(self, user_id:int, date_from:datetime, date_to:datetime):
        """
        Получает и нормализует основные бизнес-метрики за указанный период.

        Метод извлекает агрегированные показатели из базы данных и приводит
        их к формату, удобному для дальнейшего использования в API,
        аналитических отчётах и пользовательских интерфейсах.

        Выполняется преобразование типов данных и округление числовых
        значений до двух знаков после запятой.

        Args:
            user_id (int): Идентификатор пользователя.
            date_from (datetime): Начало периода анализа.
            date_to (datetime): Конец периода анализа.

        Returns:
            dict:
                Словарь с нормализованными метриками:

                - total_sessions (int) — общее количество зарядных сессий;
                - total_revenue (float) — общая выручка;
                - avg_revenue_per_station (float) — средняя выручка на одну зарядную станцию;
                - avg_revenue_per_session (float) — средняя выручка на одну зарядную сессию;
                - total_energy_kwh (float) — общий объём отпущенной энергии, кВт·ч.

        Example:
            Возвращаемое значение:

            {
                "total_sessions": 1245,
                "total_revenue": 18540.75,
                "avg_revenue_per_station": 1545.06,
                "avg_revenue_per_session": 14.89,
                "total_energy_kwh": 38250.40
            }

        Notes:
            Метод не выполняет расчёты метрик самостоятельно, а только
            преобразует и нормализует агрегированные данные,
            полученные из базы данных.
        """
        rows = await self.db.get_metrics(user_id, date_from, date_to)
        return {
            'total_sessions': int(rows["total_sessions"]),
            'total_revenue': round(float(rows["total_revenue"]), 2),
            'avg_revenue_per_station': round(float(rows["avg_revenue_per_station"]), 2),
            'avg_revenue_per_session': round(float(rows["avg_revenue_per_session"]), 2),
            'total_energy_kwh': round(float(rows["total_energy_kwh"]), 2),
        }
    
    async def get_all_normalize_metrics(
        self, 
        user_id: int, 
        date_from: datetime, 
        date_to:datetime,
        is_requested_metrics:bool=False
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
            'metrics': self.normalize_metrics(user_id, date_from, date_to),
            'station': self.normalize_connected_stations(user_id),
            'utilisation': self.calc_utilisation(user_id, date_from, date_to),
            'margin': self.get_margin_pct(user_id, date_from, date_to),
            
            
        }
        if is_requested_metrics:
            tasks['charts'] = self.normalize_metrics_chart(user_id, date_from, date_to)
            tasks['station_rating'] = self.normalize_station_rating(user_id, date_from, date_to)
        return await gather_named(tasks)
    
    async def normalize_connected_stations(self, user_id:int) -> int:
        """
        Нормализует статистику по станциям пользователя.

        Получает агрегированные данные из БД и приводит значения
        к стандартным Python-типам для последующей валидации
        через Pydantic и возврата в API.

        Returns:
            dict:
                {
                    "total_station": int,      # общее количество станций
                    "connected_stations": int  # количество станций в сети
                }
        """
        rows = await self.db.get_connected_station(user_id)
        return {
            'total_station': int(rows['total_station']),
            'connected_stations': int(rows['connected_stations'])
        }
    
    async def normalize_metrics_chart(
        self, 
        user_id:int, 
        date_from:datetime, 
        date_to:datetime
    ) -> dict:
        """
        Получает данные для графиков метрик за указанный период.

        Метод определяет необходимый уровень временной агрегации,
        запрашивает агрегированные данные из базы данных и передаёт их
        в функцию нормализации для формирования итоговой структуры.

        Args:
            user_id (int): Идентификатор пользователя.
            date_from (datetime): Начало периода анализа.
            date_to (datetime): Конец периода анализа.

        Returns:
            dict:
                Нормализованные данные для построения графиков,
                включая временную ось и значения метрик по периодам.
        """
       
        group_by = get_period_days(date_from, date_to)  
        
        date_expr = get_date_expr(group_by)
        rows = await self.db.get_charts(
            user_id, 
            date_from, 
            date_to, 
            date_expr
        )
        return _normalize_metrics_chart(group_by=group_by, rows=rows)
      
    async def normalize_station_rating(
        self,
        user_id:int,
        date_from:datetime,  
        date_to:datetime  
    ):
        rows = await self.db.get_station_revenue_stats(user_id, date_from, date_to)
        station = []
        for row in rows:
            charging_minutes=float(row['charging_minutes'])
            evse_count=float(row['evse_count'])
            utilisation = _calc_utilisation(
                charging_minutes=charging_minutes,
                evse_count=evse_count,
                date_from=date_from,
                date_to=date_to
            )
            

            station.append({
                "station_id": int(row["station_id"]),
                "station_name": row['station_name'].replace('"', '').replace("'", ''),
                "revenue": round(float(row["total_revenue"]), 2),
                "utilisation": round(utilisation, 2),
            })
        stations_sorted = sorted(
            station,
            key=lambda x: x['revenue'], 
            reverse=True
        )
        return {
            "top_stations": stations_sorted[:5],
            "worst_stations": stations_sorted[-5:][::-1],
        }


    async def get_summary_with_comparison(
        self, 
        user_id:int, 
        date_from: datetime, 
        date_to:datetime
    ) -> SummaryResponseModel:
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
        comparable_from, comparable_to = comparable_period(date_from, date_to)
        data = await gather_named({
        'requested_metrics': self.get_all_normalize_metrics(
            user_id,
            date_from,
            date_to,
            True
            ),
        'comparable_metrics': self.get_all_normalize_metrics(
            user_id,
            comparable_from,
            comparable_to
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
        # validated = SummaryResponseModel.model_validate(data)
        # return validated