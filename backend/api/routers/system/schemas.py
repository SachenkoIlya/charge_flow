from pydantic import BaseModel
from datetime import datetime


class SystemSchema(BaseModel):
    mode: str


class MonitoringSchema(BaseModel):
    user_id: int
    type_method: str
    run_mode: str
    operator: str
    status: str
    last_success_at: datetime | None = None
    created_at: datetime | None = None
    run_id: str | None = None
    error: str | None = None
    updated_at: datetime | None = None
    processed_at: datetime | None = None
    
class EtlRunsResponseSchema(BaseModel):
    rows: list[MonitoringSchema]