from pydantic import BaseModel, ValidationError
from typing import Optional
from nicegui import ui
from core.logger.logger import logger
from datetime import date

class OpexSchema(BaseModel):
    station_id: int
    expense_date: Optional[str] = None
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
    expense_date: Optional[str] = None
    location_search: Optional[float] = None
    equipment_purchase: Optional[float] = None
    construction_and_installation: Optional[float] = None
    other_capex: Optional[float] = None
    comment: Optional[str] = None


schemas = {
    'opex': OpexSchema,
    'capex': CapexSchema
}


def resolve_model(payload:dict, mode:str):
    schema = schemas.get(mode)
    try:
        return schema.model_validate(payload)
    except ValidationError as v:
        logger.error(str(v))
        ui.notify('Проверьте корректность введённых сумм', color='red')
