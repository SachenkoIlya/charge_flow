from pydantic import BaseModel, Field, ValidationError
from typing import Literal
from datetime import datetime, timezone
from uuid import uuid4


class RunConfig(BaseModel):
    run_mode: Literal['test', 'dev', 'prod'] 
    operator: Literal['volt']
    type_method: str | None = None
    user_id: int | None = None
    
class RunContextMeta(BaseModel):
    run_id: str = Field(default_factory=lambda: uuid4().hex)
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
