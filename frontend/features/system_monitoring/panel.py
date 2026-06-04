
from frontend.components.drawer import render_sidebar
from frontend.api.client import frontend_api
from frontend.components.render_title import render_title
from frontend.features.base.panel import BasePanel 
from fastapi import Request
from nicegui import ui, app
from copy import deepcopy
from dataclasses import dataclass
from frontend.features.system_monitoring.render.tables import render_table
from core.logger.logger import logger

@dataclass
class Panel(BasePanel):
    user: dict
    request: Request
    endpoint_name: str = 'system'
    page_key = 'system'


    async def render(self):
        page = app.storage.user.setdefault('pages', {})
        page_state = page.setdefault(self.page_key, {})
        
        if page_state.get('toggle_value') is None:
            page_state['toggle_value'] = 'etl_run'
        
        self.apply_filters()
        loaded = await self.load_data()
        if not loaded:
            return
        
        role = self.user.get('role')

        with ui.element('div').classes(
            """
                w-screen
                h-screen
                flex
                bg-gradient-to-br
                from-[#050b12]
                via-[#08111b]
                to-[#0b1724]
                text-white
                overflow-hidden
            """
        ):
            render_sidebar(role=role)
            with ui.element('main').classes(
                """
                    flex-1
                    h-screen
                    overflow-hidden
                    px-10
                    py-2
                """
            ) as self.container:
                await self.render_content()



    async def render_content(self):
        

        page = app.storage.user.get('pages', {})
        page_state = page.get(self.page_key, {})
        
        toggle_value = page_state.get('toggle_value', 'etl_run')

        await render_title(
            label='Мониторинг системы',
            label_aggre='system monitoring',
            page_key=self.page_key,
            on_date_change=self.on_date_change,
        )
        render_table(
            mode=toggle_value,
            rows=self.data.get('rows', []),
            height=700
        )

    async def load_data(self):
        payload = deepcopy(self.payload)
        payload['mode'] = payload.pop('toggle_value', None)
        

        data = await frontend_api(
            endpoint_name=self.endpoint_name,
            payloads=payload,
            request=self.request
        )
        
        if data is None:
            self.data = {}
            return False
        
        self.data = data
        return True