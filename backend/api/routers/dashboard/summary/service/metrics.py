


from backend.api.routers.dashboard.finance.service.conext import PeriodContext
from backend.api.routers.dashboard.summary.db import SummaryDB
from  asyncpg import Record

class Metrics:
    def __init__(self, repository: "SummaryDB"):
        self.repository = repository

    @staticmethod
    def _normalize_metrics(rows: Record | None) -> dict:
        return {
            'total_sessions': int(rows["total_sessions"]),
            'total_revenue': round(float(rows["total_revenue"]), 2),
            'avg_revenue_per_station': round(float(rows["avg_revenue_per_station"]), 2),
            'avg_revenue_per_session': round(float(rows["avg_revenue_per_session"]), 2),
            'total_energy_kwh': round(float(rows["total_energy_kwh"]), 2),
        }

    async def get_metrics(
        self, 
        ctx: PeriodContext
    ) -> dict:
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
        rows = await self.repository.get_metrics(
            user_id=ctx.user_id, 
            date_from=ctx.date_from, 
            date_to=ctx.date_to,
            station_ids=ctx.station_ids
        )
        return self._normalize_metrics(rows)