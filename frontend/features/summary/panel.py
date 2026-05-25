from frontend.features.base.panel import BasePanel
from frontend.components.drawer import render_sidebar
from frontend.api.client import frontend_api

from dataclasses import dataclass
from copy import deepcopy
from fastapi import Request
from nicegui import ui

from frontend.features.summary.render.title import render_title



@dataclass
class Panel(BasePanel):
    user: dict
    request: Request
    endpoints_name: str = 'summary'
    page_key = 'summary'

    async def render(self):
        self.apply_filters()
        # loaded = await self.load_data()
        # if not loaded:
        #     return
        
        role = self.user.get('role')

        with ui.element('div').classes(
            'w-screen min-h-screen flex bg-gradient-to-br from-[#050b12] via-[#08111b] to-[#0b1724] text-white overflow-hidden'
        ):
            render_sidebar(role=role)
        
            with ui.element('main').classes(
                    # 'w-full max-w-[2000px] mx-auto px-7 mt-10'
                        """
                            flex-1
                            px-8
                            py-8
                            flex
                            items-center
                            justify-center
                        """
                ) as self.container:
                    await self.render_content()



    async def render_content(self):
        # metrics = get_metrics(self.data)
        # chart = self.data['chart']
        
        label = 'Общая сводкка по сети'
        style: str = None
        label_aggre: str = None
        with ui.element('div').classes('w-full max-w-[1700px]'):
            render_title(
                label='Общая сводка по сети',
                label_aggre='Executive Dashboard'
            )