from pydantic import BaseModel, Field
from typing import Literal, Optional

class DashboardFilterSchema(BaseModel):
    period: Literal['one_month'] = Field(
        description='Период отчета. Для оперативной сводки доступен только текущий месяц с сравнением с предыдущим.',
        examples=['one_month'],
    )
    station_ids: list[int] = Field(
        default_factory=list,
        description='Список идентификаторов станций. Пустой список — все станции.',
        examples=[[], [138, 139]],
    )


# class DashboardFilterSchema(BaseModel):
#     date_from: Optional[str] = Field(
#         description="Дата начала периода в формате DD.MM.YYYY",
#         examples=["01.04.2026"],
#     )
#     date_to: Optional[str] = Field(
#         description="Дата окончания периода в формате DD.MM.YYYY",
#         examples=["30.04.2026"],
#     )
  

    # company_id: Optional[int] = None
