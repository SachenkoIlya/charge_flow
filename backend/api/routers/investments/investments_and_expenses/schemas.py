from pydantic import BaseModel
from core.logger.logger import logger
from typing import Literal


class InvestmentExpenseCreateSchema(BaseModel):
    mode: Literal['capex', 'opex']

    station_id: int
    expense_date: str | None = None
    # CAPEX
    location_search: float | None = None
    equipment_purchase: float | None = None
    construction_and_installation: float | None = None
    other_capex: float | None = None

    # OPEX
    electricity_compensation: float | None = None
    rent_payment: float | None = None
    operator_commission: float | None = None
    internet_and_connection: float | None = None
    taxes: float | None = None
    insurance: float | None = None
    service_maintenance: float | None = None
    other_expenses: float | None = None

    comment: str | None = None