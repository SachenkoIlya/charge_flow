
from frontend.components.drawer import render_sidebar
from frontend.components.render_title import render_title
from frontend.components.metric_card import render_metrics 
from frontend.features.base.panel import BasePanel

from frontend.features.finance.charts.render_charts import render_finance_charts


from frontend.api.client import frontend_api

from frontend.features.finance.render.metrics import FINANCE_METRICS
from frontend.features.finance.charts.cashflow import CASHFLOW_METRICS
from frontend.features.finance.charts.break_even import BREAK_EVEN_METRICS
from frontend.features.finance.charts.cost_structure import COST_STRUCTURE
from frontend.features.finance.charts.tables_section import (
    render_tables_section, 
    PLAN_FACT_ROWS, 
    PNL_ROWS
)

from dataclasses import dataclass
from copy import deepcopy
from fastapi import Request
from nicegui import ui




@dataclass
class Panel(BasePanel):
    user: dict
    request: Request
    endpoints_name: str = 'finance'
    page_key = 'finance'

    
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
                        """
                            flex-1
                            h-screen
                            overflow-hidden
                            px-8
                            py-2
                        """
                ) as self.container:
                    await self.render_content()



    async def render_content(self):
        with ui.element('div').style('zoom: 0.8'):
            await render_title(
                label='Фиинансы и прибыльность',
                label_aggre='Finance & Profitability',
                page_key=self.page_key,
                on_date_change=self.on_date_change 
            )
            render_metrics(
                metrics=FINANCE_METRICS, 
                columns=len(FINANCE_METRICS)
            )
            
            render_finance_charts(
                cashflow=CASHFLOW_METRICS,
                break_even=BREAK_EVEN_METRICS,
                cost_structure=COST_STRUCTURE
            )
            render_tables_section(
                rows=PNL_ROWS,
                plan_rows=PLAN_FACT_ROWS
            )