from pydantic import BaseModel, EmailStr
from typing import Optional

class ConnectOperator(BaseModel):
    email: EmailStr
    password: str
    login: str
    operator: Optional[str] = 'volt'