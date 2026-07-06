from pydantic import BaseModel, Field
from typing import Literal

# Параметры для структуры затрат
class NetworkCostStructureParams(BaseModel):
    period: Literal['all', '6m', '1y'] = Field(
        default='6m', 
        description="Временной период для анализа расходов"
    )
    station_ids: list[int] = Field(
        default=[], 
        description="Список ID станций для фильтрации"
    )

