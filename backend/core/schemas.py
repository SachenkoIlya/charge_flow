from pydantic import BaseModel, Field
from typing import Optional


class DashboardFilterSchema(BaseModel):
    date_from: Optional[str] = Field(
        description="Дата начала периода в формате DD.MM.YYYY",
        examples=["01.04.2026"],
    )
    date_to: Optional[str] = Field(
        description="Дата окончания периода в формате DD.MM.YYYY",
        examples=["30.04.2026"],
    )
  

    # company_id: Optional[int] = None
