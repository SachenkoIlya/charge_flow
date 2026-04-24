from pydantic import BaseModel, EmailStr
from typing import Optional

class DashboardFilterSchema(BaseModel):
    date_from: str | None
    date_to: str | None
    company_id: Optional[int] = None

class MetricItemSchema(BaseModel):
    label: str 
    value: float | str
    color: Optional[str] = None



class MetricsBlockSchema(BaseModel):
    total_revenue: float
    my_revenue: float
    operator_revenue: float
    operator_percent: float
    total_energy_kwh: float
    average_bill: float
    total_users: int
    avg_charge_time: float
    success_sessions: int
    total_sessions: int

class ChartItemSchema(BaseModel):
    name: str
    value: float

class StatsResponseSchema(BaseModel):
    metrics: MetricsBlockSchema
    chart: list[ChartItemSchema]
    total_station: int
    meta: dict