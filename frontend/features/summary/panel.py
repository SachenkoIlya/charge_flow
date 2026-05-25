from frontend.features.base.panel import BasePanel
from frontend.components.drawer import render_sidebar
from frontend.api.client import frontend_api
from frontend.features.summary.render.charts import render_chart, CHART_METRICS
from frontend.features.summary.render.metrics import render_metrics, METRICS
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
                    # 'w-full max-w-[2000px] mx-auto px-7 mt-10'
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
            render_metrics(METRICS)
            render_chart(CHART_METRICS)