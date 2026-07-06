
from backend.api.routers.widget.charts.network_cost_structure.shemas import NetworkCostStructureParams
from pydantic import BaseModel, Field

from backend.api.routers.widget.charts.summary_time_series.schemas import SummaryTimeSeriesParams  


class ChartsRequestSchema(BaseModel):
    """
    Схема входящих данных для пакетного запроса графиков панели управления.
    
    Каждое поле соответствует конкретному типу графика. Если поле передано 
    (не равно None), бэкенд рассчитает и вернет этот график в ответе. Это позволяет 
    фронтенду гибко запрашивать один или несколько чартов в рамках одного HTTP-запроса.
    """
    network_cost_structure: NetworkCostStructureParams | None = Field(
        default=None,
        description="Параметры для графика структуры затрат сети. Если null — график не рассчитывается."
    )
    summary_time_series:  SummaryTimeSeriesParams | None = Field(
        default=None,
        description="Параметры для графика суммарного временного ряда метрик (Time Series). Если null — график не рассчитывается."
    )

   