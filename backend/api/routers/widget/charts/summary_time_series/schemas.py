from pydantic import BaseModel, Field, model_validator
from datetime import date

class PeriodParams(BaseModel):
    """
    Схема параметров временного периода.

    Определяет границы временного отрезка для фильтрации данных. Включает в себя
    модельную валидацию, предотвращающую передачу некорректного диапазона, 
    где дата начала превышает дату конца.
    """
    date_from: date = Field(
        description="Начальная дата периода (включительно) в формате YYYY-MM-DD",
        examples=["2026-04-01"]
    )
    date_to: date = Field(
        description="Конечная дата периода (включительно) в формате YYYY-MM-DD",
        examples=["2026-05-01"]
    )
    @model_validator(mode='after')
    def validate_range(self):
        """
        Проверяет, что начальная дата не позже конечной даты.

        Raises:
            ValueError: Если date_from строго больше, чем date_to.
        """
        if self.date_from > self.date_to:
            raise ValueError("date_from cannot be greater than date_to")
        return self


class SummaryTimeSeriesParams(BaseModel):
    """
    Параметры фильтрации для получения суммарного временного ряда (Time Series).

    Объединяет в себе настройки временного диапазона и фильтрацию по физическим 
    объектам (станциям) для построения детальных графиков на дашборде.
    """
    period: PeriodParams = Field(
        description="Период анализа временного ряда (диапазон дат)"
    )

    station_ids: list[int] = Field(
        default_factory=list,
        description="Список ID станций для фильтрации данных временного ряда"
    )