from dataclasses import dataclass
from datetime import timedelta

@dataclass
class ReportPolicy:
    name: str
    first_run_days_back: int
    paid_interval: timedelta | None = None
   