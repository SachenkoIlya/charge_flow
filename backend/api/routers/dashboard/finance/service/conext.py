from datetime import datetime
from typing import Optional 
from dataclasses import dataclass


@dataclass(frozen=True)
class PeriodContext:
    user_id: int
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    period: str = None
    station_ids: list[int] = None
