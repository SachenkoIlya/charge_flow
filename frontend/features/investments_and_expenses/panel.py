from dataclasses import dataclass
from fastapi import Request
from frontend.components.drawer import render_sidebar
from frontend.components.render_title import render_title
from frontend.features.base.panel import BasePanel
from nicegui import ui, app
from core.logger.logger import logger
from copy import deepcopy


@dataclass
class Panel(BasePanel):
    user: dict
    request: Request
    endpoints_name: str = 'investments_and_expenses'
    page_key = 'investments_and_expenses'

    
    async def render(self):
        page = app.storage.user.setdefault('pages', {})
        page_state = page.setdefault(self.page_key, {})

        page_state.setdefault('toggle_value', 'CAPEX')
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
         with ui.element('div').style('zoom: 1'):
            await render_title(
                label='CAPEX & OPEX',
                label_aggre='Инвестиции и операционные расходы',
                page_key=self.page_key,
                on_date_change=self.on_date_change 
            )
    
    async def load_data(self):
        payload = deepcopy(self.payload)
        logger.debug(f"{self.page_key}: зашли в load_data".upper())
        logger.debug(f"payload: {payload}")
        return True

        