
from frontend.components.drawer import render_sidebar

from frontend.features.base.panel import BasePanel
from frontend.features.summary.render.tables_section import (
    render_tables_section, 
    TOP_ROWS, 
    REVERS_ROWS
)
from frontend.features.summary.render.charts import render_chart
from core.logger.logger import logger

from frontend.components.metric_card import render_metrics 
from frontend.components.render_title import render_title

from dataclasses import dataclass
from fastapi import Request
from nicegui import ui, app



@dataclass
class Panel(BasePanel):
    user: dict
    request: Request
    endpoints_name: str = 'summary'
    page_key = 'summary'

    async def render(self):
        self.reset_page_dates()
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
        with ui.element('div').classes('text-[80%]'):
            await render_title(
                label='Общая сводка по сети',
                label_aggre='Executive Dashboard',
                page_key=self.page_key,
                on_date_change=self.on_date_change,
            )

            render_metrics(data=self.data, columns=5)
            render_chart(data=self.data)
            render_tables_section(TOP_ROWS, REVERS_ROWS)

    
        