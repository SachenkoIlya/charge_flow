
from frontend.components.drawer import render_sidebar
from datetime import datetime, timedelta
from core.logger.logger import logger
from frontend.features.base.panel import BasePanel
from frontend.features.summary.render.render_top_table import render_top_tables_dialog
from frontend.features.summary.render.metrics import (
    METRICS, 
    get_metric_value, 
    get_metric_delta
)
from frontend.features.summary.render.charts import render_chart

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
        selected_station = await self.get_selected_stations()
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
                    min-h-screen
                    overflow-y-auto
                    overflow-x-hidden
                    px-6
                    py-5
                """
            ) as self.container:
                await self.render_content(stations=selected_station)



    async def render_content(self, stations: list[dict]):

        logger.debug(stations)

        comparable_period = self.data['comparable_period']

        
        comparable_from = datetime.strptime(
            comparable_period['date_from'],
            '%Y-%m-%d %H:%M:%S'
        ).strftime('%d.%m.%Y')

        comparable_to = (
            datetime.strptime(
                comparable_period['date_to'],
                '%Y-%m-%d %H:%M:%S'
            ) - timedelta(days=1)
        ).strftime('%d.%m.%Y')

        label_aggre = (
            f"Сравниваемый период: "
            f"{comparable_from} — {comparable_to}"
        )

        with ui.column().classes('w-full max-w-[1600px] mx-auto gap-3'):
            await render_title(
                label='Общая сводка по сети',
                label_aggre=label_aggre,
                page_key=self.page_key,
                stations=stations,
                on_date_change=self.on_date_change,
            )
            top_dialog = render_top_tables_dialog(self.data)
            render_metrics(
                data=self.data, 
                columns=5,  
                metric_value_func=get_metric_value, 
                metric_delta_func=get_metric_delta,
                default_metrics=METRICS,
                on_top_click=top_dialog.open
                )
            render_chart(data=self.data)
            # render_tables_section(TOP_ROWS, REVERS_ROWS)

    
        