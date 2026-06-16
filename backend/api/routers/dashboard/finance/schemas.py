from typing import Optional
from pydantic import BaseModel, Field


class FinanceFilterSchema(BaseModel):
    toggle_value: Optional[str] = Field(
        description=(
            "Период отчета. Возможные значения: "
            "'6m' (6 месяцев), "
            "'1y' (1 год), "
            "'all' (весь период). "
            "Допускается null."
        ),
        examples=['all'],
    )