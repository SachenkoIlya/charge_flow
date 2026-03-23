from dataclasses import dataclass
from typing import Optional
from datetime import datetime




@dataclass
class Users:
    id: int        
    name: str       
    operator: str   
    auth_type: str  
    is_active: bool   
    created_at: datetime 
    account_type: str
    role: str       
    paid_until: Optional[datetime] = None
    login: Optional[str] = None
    password: Optional[str] = None
    api_key: Optional[str] = None

    @classmethod
    def from_db(cls, row):
        return cls(**dict(row))
    

    @property
    def full_name(self):
        return f"{self.id}/{self.name}"

