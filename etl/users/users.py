from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from core.security.security import security

@dataclass
class UserCredentials:
    id: int
    auth_type: str
    is_active: bool
    operator: str
    created_at: datetime
    updated_at: datetime
    paid_until: Optional[datetime] = None
    login: Optional[str] = field(default=None, repr=False)
    password: Optional[str] = field(default=None, repr=False)
    api_key: Optional[str] = field(default=None, repr=False)
  

    @classmethod
    def from_db(cls, row):
        return cls(
            id=row['user_id'],
            is_active=row['is_active'],
            operator=row['operator'], # Исправил присвоение
            created_at=row['created_at'],
            auth_type=row['auth_type'],
            updated_at=row['updated_at'],
            paid_until=row['paid_until'],
            login=security.decrypt_data(row['login']),
            password=security.decrypt_data(row['password']),
            api_key=security.decrypt_data(row['api_key']) if row['api_key'] else None,
        )
    

    @property
    def full_name(self):
        return f"{self.id}/{self.login}"

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

