
from frontend.components.drawer import render_sidebar
from frontend.components.render_title import get_data_from_map, render_title
from frontend.components.metric_card import render_metrics 
from frontend.features.base.panel import BasePanel

from frontend.features.finance.charts.render_charts import render_finance_charts
from frontend.features.finance.render.metrics import (
    FINANCE_METRICS,
    get_metrics_value,
    get_metric_delta
)

from frontend.features.finance.render.metrics import FINANCE_METRICS
from frontend.features.finance.charts.break_even import BREAK_EVEN_METRICS

from dataclasses import dataclass
from fastapi import Request
from nicegui import ui, app




@dataclass
class Panel(BasePanel):
    user: dict
    request: Request
    endpoints_name: str = 'finance'
    page_key = 'finance'

    
    async def render(self):
        await self.load_station()

        page = app.storage.user.setdefault('pages', {})
        page_state = page.setdefault(self.page_key, {})
        
        data = get_data_from_map(self.page_key)
        if data and page_state.get('toggle_value') is None:
            page_state['toggle_value'] = data['default_value']
       
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
        charts = self.data['charts']

        # with ui.element('div').style('zoom: 0.9'):
        with ui.column().classes('w-full max-w-[1600px] mx-auto gap-2'):
            await render_title(
                label='Финансы и прибыльность',
                # label_aggre='Finance & Profitability',
                stations=self.stations,
                page_key=self.page_key,
                on_date_change=self.on_date_change 
            )
            render_metrics(
                self.data, 
                columns=len(FINANCE_METRICS),
                metric_value_func=get_metrics_value, 
                metric_delta_func=get_metric_delta,
                default_metrics=FINANCE_METRICS,
            )

            render_finance_charts(
                cash_flow_history=charts['cash_flow_history'],
                break_even=BREAK_EVEN_METRICS,
                cost_structure=charts['network_cost_structure']
            )
            
            # render_tables_section(
            #     rows=PNL_ROWS,
            #     plan_rows=PLAN_FACT_ROWS
            # )



        