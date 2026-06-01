from pydantic import BaseModel
from typing import Optional


class OpexSchema(BaseModel):
    station_id: int
    electricity_compensation: Optional[float] = None
    rent_payment: Optional[float] = None
    operator_commission: Optional[float] = None
    internet_and_connection: Optional[float] = None
    taxes: Optional[float] = None
    insurance: Optional[float] = None
    service_maintenance: Optional[float] = None
    other_expenses: Optional[float] = None
    comment: Optional[str] = None


class CapexSchema(BaseModel):
    station_id: int
    location_search: Optional[float] = None
    equipment_purchase: Optional[float] = None
    construction_and_installation: Optional[float] = None
    other_capex: Optional[float] = None
    comment: Optional[str] = None


schemas = {
    'opex': OpexSchema,
    'capex': CapexSchema
}