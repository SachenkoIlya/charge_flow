from dataclasses import dataclass
from fastapi import Request
from frontend.components.header import  get_header
from frontend.components.drawer import get_drawer

@dataclass
class Panel:
    user: dict
    request: Request
    endpoints_name = 'trends'


    def __post_init__(self):
        self.data = None
    
    async def render(self):
        role = self.user.get('role')
        drawer = get_drawer(role=role)
        await get_header(drawer=drawer, role=role, request=self.request)