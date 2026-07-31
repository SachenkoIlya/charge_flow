from backend.api.routers.dashboard.summary.service.charts import Charts
from backend.api.routers.widget.charts.db import ChartsDB
from core.base_db import Base
from datetime import datetime

# from backend.api.routers.dashboard.summary.service.charts import _normalize_metrics_chart
from backend.utils.period_date import (
    get_period_days,
    get_date_expr,
)


class SummaryTimeSeries:
    def __init__(self, chart_db: "ChartsDB"):
        self.db = chart_db
        self.chart_name: str = 'summary_time_series'
    
    async def build(
        self, 
        user_id:int, 
        period:dict,
       
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

        period_date = period.get('period')
        date_from = period_date.get('date_from') 
        date_to = period_date.get('date_to')
        
        group_by = get_period_days(date_from, date_to)  
        date_expr = get_date_expr(group_by)
        
        rows = await self.db.get_metrics_time_series(
            user_id, 
            date_from, 
            date_to, 
            date_expr
        )
        result =  Charts._normalize_metrics_chart(group_by=group_by, rows=rows)
        result['date_range'] = {
            'period_mode': None,
            'group_by': group_by,
            'date_from': date_from.strftime("%Y-%m-%d"),
            'date_to': date_to.strftime("%Y-%m-%d"),
        }
        return result 