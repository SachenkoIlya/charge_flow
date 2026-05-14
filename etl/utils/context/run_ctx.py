from typing import TYPE_CHECKING
from datetime import datetime
from dataclasses import dataclass



if TYPE_CHECKING:
    from etl.users.users import UserCredentials



@dataclass
class RunContext:
    user: "UserCredentials"
    now: datetime
    last_success: datetime | None
