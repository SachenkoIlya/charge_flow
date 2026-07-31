from pydantic import BaseModel, Field
from typing import Literal



class FinanceRequestModel(BaseModel):
    period: Literal["6m", "1y", "all"] = Field(
        description=(
            "Период отчёта: '6m' — 6 месяцев, "
            "'1y' — 1 год, 'all' — весь период."
        ),
        examples=["all"],
    )
    station_ids: list[int] = Field(
        default_factory=list,
        description='Список идентификаторов станций. Пустой список — все станции.',
        examples=[[], [138, 139]],
    )

    