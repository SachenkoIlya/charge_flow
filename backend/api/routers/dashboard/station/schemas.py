from pydantic import BaseModel, Field
from typing import Literal

# для запроса метрик 
class StationSchemas(BaseModel):
    label: str
    stations_count: int
    station_ids: list[int]
    station_keys: list[str]