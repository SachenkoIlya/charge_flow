from typing import TYPE_CHECKING
from datetime import datetime
from dataclasses import dataclass



if TYPE_CHECKING:
    from backend.users.users import Users



@dataclass
class RunContext:
    user: "Users"
    now: datetime
    last_success: datetime | None
