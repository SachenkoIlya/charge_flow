from asyncpg import Record
from datetime import datetime, timedelta
from backend.api.routers.dashboard.finance.service.conext import PeriodContext
from backend.api.routers.dashboard.summary.db import SummaryDB
from backend.utils.period_date import (
    get_period_days,
    get_date_expr,
)

class Charts:
    def __init__(self, repository: "SummaryDB"):
        self.repository = repository

    @staticmethod
    def get_label_and_utilisation_pct(
        group_by:str, 
        charging_minutes:float, 
        period:datetime, 
        evse_count:float
    )-> dict:
        """
        Формирует подпись периода и рассчитывает коэффициент утилизации.

        В зависимости от типа группировки определяет длительность
        временного интервала, формирует человекочитаемую подпись
        для графика и вычисляет процент утилизации зарядной инфраструктуры.

        Args:
            group_by (str): Тип группировки (`day`, `week`, `month`).
            charging_minutes (float): Суммарное время зарядки за период в минутах.
            period (datetime): Дата начала периода.
            evse_count (float): Количество доступных EVSE.

        Returns:
            dict:
                Словарь со значениями:

                - label (str) — подпись периода для графика;
                - utilisation_pct (float) — коэффициент утилизации в процентах.

        Notes:
            Утилизация рассчитывается по формуле:

                charging_minutes /
                (evse_count * bucket_minutes) * 100

            где `bucket_minutes` — продолжительность периода
            в минутах (день, неделя или месяц).
        """
        if group_by == 'day':
            bucket_minutes = 1440
            label = period.strftime("%d.%m")

        elif group_by == 'week':
            bucket_minutes = 7 * 1440
            label = period.strftime("%d.%m")

        else:
            next_month = (
                period.replace(day=28) + timedelta(days=4)
            ).replace(day=1)

            bucket_minutes = (
                next_month - period
            ).total_seconds() / 60

            label = period.strftime("%m.%Y")
                
        available_minutes = evse_count * bucket_minutes
        utilisation_pct = (
            charging_minutes / available_minutes * 100
            if available_minutes > 0
            else 0
        )
        return {
            'label': label,
            'utilisation_pct': utilisation_pct
        }
    
    @staticmethod
    def _normalize_metrics_chart(rows: list[Record], group_by:str)-> dict:
        """
        Преобразует агрегированные данные в формат, пригодный для построения графиков.

        Для каждого периода формирует подпись временной оси, рассчитывает
        коэффициент утилизации и собирает значения метрик в отдельные серии.

        Args:
            rows (list[asyncpg.Record]): Агрегированные данные по периодам.
            group_by (str): Тип группировки (`day`, `week`, `month`).

        Returns:
            dict:
                Словарь с данными для визуализации:

                - xAxis (list[str]) — подписи временной оси;
                - series.revenue (list[float]) — выручка по периодам;
                - series.sessions (list[int]) — количество сессий по периодам;
                - series.utilisation (list[float]) — коэффициент утилизации по периодам.

        Notes:
            Для расчёта подписей периодов и утилизации используется
            функция `get_label_and_utilisation_pct()`.
        """
        x_axis, revenue, sessions, utilisation = [], [], [], []
        
        for row in rows:
            period = row["period"]
            evse_count = float(row["evse_count"])
            charging_minutes = float(row["charging_minutes"])
                
            metrics_chart = Charts.get_label_and_utilisation_pct(
                group_by,
                charging_minutes,
                period,
                evse_count
            )

            x_axis.append(metrics_chart['label'])
            revenue.append(round(float(row["revenue"]), 2))
            sessions.append(int(row["sessions"]))
            utilisation.append(round(metrics_chart['utilisation_pct'], 2))

        return {
            'xAxis': x_axis,
            'series': {
                "revenue": revenue,
                "sessions": sessions,
                "utilisation": utilisation,
            },
        }

    async def get_metrics_chart(
        self, 
        ctx: PeriodContext
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
           
        group_by = get_period_days(ctx.date_from, ctx.date_to)  
        date_expr = get_date_expr(group_by)
            
        rows = await self.repository.get_charts(
            user_id=ctx.user_id, 
            date_from=ctx.date_from, 
            date_to=ctx.date_to, 
            station_ids=ctx.station_ids, 
            date_expr=date_expr
        )
        return self._normalize_metrics_chart(group_by=group_by, rows=rows)



