from dataclasses import dataclass
from fastapi import Request
from frontend.components.header import  get_header
from frontend.components.drawer import get_drawer
from nicegui import ui
from frontend.features.base.panel import BasePanel
from frontend.features.trends.renders.high import render_high
from frontend.features.trends.renders.middle import render_middle
from frontend.features.trends.renders.low import render_low

@dataclass
class Panel(BasePanel):
    user: dict
    request: Request
    endpoints_name: str = 'trends'
    page_key: str = 'trends'

  
    
    async def render(self):
        self.role = self.user.get('role')
        drawer = get_drawer(role=self.role)
        
        await get_header(
            request=self.request,
            drawer=drawer,
            on_date_change=self.on_date_change,
            page_key=self.page_key,
            refresh=self.refresh,
            role=self.role
        )
        with ui.element('div').classes('w-full max-w-[2000px] mx-auto px-7 mt-3') as self.container:
            await self.render_content()

    async def render_content(self):
        with ui.element('div').style(
            'display: flex; flex-direction: column; gap: 10px; width: 100%;'
        ):
            await render_high()
            await render_middle()
            await render_low()

    # тест
    



                    
     