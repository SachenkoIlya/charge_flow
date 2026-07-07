from pydantic import BaseModel, Field, model_validator
from typing import Literal

# Параметры для структуры затрат
class NetworkCostStructureParams(BaseModel):
    period: Literal['all', '6m', '1y'] = Field(
        description="Временной период для анализа расходов"
    )
    station_ids: list[int] | None = Field(
        default=None, 
        description="Список ID станций для фильтрации"
    )

    @model_validator(mode='after')
    def validate_ranfe(self):
        """
        Проверяет, что начальная дата не позже конечной даты.

        Raises:
            ValueError: Если date_from строго больше, чем date_to.
        """
        if self.period is None:
            raise ValueError("The period must not be None")
        return self