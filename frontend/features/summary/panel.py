
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
from frontend.components.render_title import get_data_from_map, render_title

from dataclasses import dataclass
from fastapi import Request
from nicegui import ui, app



@dataclass
class Panel(BasePanel):
    user: dict
    request: Request
    endpoints_name: str = 'summary'
    page_key = 'summary'

    @staticmethod
    def format_date(
        dates:str,
        date_str: str="%d.%m.%Y",
        date_time_str:str="%Y-%m-%d %H:%M:%S"
    ):
        return datetime.strptime(
            dates, date_time_str
        ).strftime(date_str)
    
    async def render_content(self):
        requested_period = self.data['requested_period']
        comparable_period = self.data['comparable_period']

        current_from = self.format_date(requested_period['date_from'])
        current_to = self.format_date(requested_period['date_to'])
        comparable_from = self.format_date(comparable_period['date_from'])
        comparable_to = self.format_date(comparable_period['date_to'])

        current_period = (
            f"Текущий период: "
              f"{current_from} — {current_to}"
        )

        сomparison_period = (
            f"Сравниваемый период: "
            f"{comparable_from} — {comparable_to}"
        )

        with ui.column().classes('w-full max-w-[1600px] mx-auto gap-3'):
            await render_title(
                label='Оперативная Сводка',
                current_period=current_period,
                сomparison_period=сomparison_period,
                page_key=self.page_key,
                stations=self.stations,
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

    
        