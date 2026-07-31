from pydantic import BaseModel, EmailStr
from typing import Optional

class ConnectOperatorRequest(BaseModel):
    email: EmailStr
    password: str
    login: str
    operator: Optional[str] = 'volt'