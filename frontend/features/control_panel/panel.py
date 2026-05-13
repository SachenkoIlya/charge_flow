from frontend.features.control_panel.renders.left import render_left
from frontend.features.control_panel.renders.right import render_right
from frontend.features.control_panel.metrics import get_metrics
from frontend.features.base.panel import BasePanel
from frontend.components.header import get_header
from frontend.components.drawer import get_drawer
from frontend.api.client import frontend_api

from dataclasses import dataclass
from copy import deepcopy
from fastapi import Request
from nicegui import ui




@dataclass
class Panel(BasePanel):
    user: dict
    request: Request
    endpoints_name: str = 'dashboard_stats'
    page_key = 'control_panel'
    
    async def render(self):
        self.apply_filters()
        loaded = await self.load_data()
        if not loaded:
            return
        
        role = self.user.get('role')
        drawer = get_drawer(role=role)
        
        await get_header(
            request=self.request,
            drawer=drawer,
            apply_filters=self.apply_filters,
            on_date_change=self.on_date_change,
            page_key=self.page_key,
            refresh=self.refresh,
            role=role
        )
        
        with ui.element('div').classes('w-full max-w-[2000px] mx-auto px-7 mt-10') as self.container:
            await self.render_content()
    
    async def render_content(self):
        metrics = get_metrics(self.data)
        chart = self.data['chart']
        
        with ui.element('div').style('display: flex; gap: 15px; width: 100%; align-items: stretch; min-height: 650px'):
            await render_left(metrics, chart)
            await render_right(metrics)



    async def load_data(self):
        payload = deepcopy(self.payload)
        
        if self.company_id:
            payload['company_id'] = self.company_id

        data = await frontend_api(
            endpoint_name=self.endpoints_name,
            payloads=payload,
            request=self.request,
        )
        if data is None:
            self.data = {}
            return False

        self.data = data
        return True
        