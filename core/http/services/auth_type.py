from dataclasses import dataclass
import base64
from typing import Literal
import aiohttp

AuthKind = Literal["basic", "bearer"]


@dataclass
class AuthType:
    auth_type: AuthKind
    login: str
    password: str
    api_key: str


    def get_auth_headers(self) -> dict:
        """Универасльный headrs. 
            Вовмируем заголоовки для aiohttp запросса
            auth_type может быть Authorization или Base
            если base декодируем {'login': 'password'} в base64 
        """
        if self.auth_type == 'basic':
            if not self.login or not self.password:
                raise ValueError("Basic auth требует login и password")
            auth_str = f"{self.login}:{self.password}"
            encoded = base64.b64encode(auth_str.encode('utf-8')).decode()
            # return {'Authorization': f"Basic {encoded}"}, encoded
            return  {
                'headers': None,
                'aiohttp_auth': aiohttp.BasicAuth(self.login, self.password),
                'token': encoded
            }
        if self.auth_type == 'bearer':
            if not self.api_key:
                raise ValueError("Bearer auth требует api_key")
            return {
                'headers': {'Authorization': f"Bearer {self.api_key}"},
                'aiohttp_auth': None,
                'token': self.api_key
            }
        
        raise ValueError(f"Неизвестный auth_type: {self.auth_type}")
