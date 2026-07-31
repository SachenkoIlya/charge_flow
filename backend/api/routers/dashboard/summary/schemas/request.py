from pydantic import BaseModel, Field
from typing import Literal

class SummaryRequestModel(BaseModel):
    period: Literal['one_month'] = Field(
        description='Период отчета. Для оперативной сводки доступен только текущий месяц с сравнением с предыдущим.',
        examples=['one_month'],
    )
    station_ids: list[int] = Field(
        default_factory=list,
        description='Список идентификаторов станций. Пустой список — все станции.',
        examples=[[], [138, 139]],
    )


    