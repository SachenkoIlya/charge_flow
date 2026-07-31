from nicegui import ui

from frontend.components.pnl_table import render_pnl_table
from frontend.features.finance.charts.cashflow import render_cashflow_chart
from frontend.features.finance.charts.break_even import render_break_even_chart
from frontend.features.finance.charts.cost_structure import render_cost_structure_chart


# def render_finance_charts(
#     cash_flow_history :list[dict]=None, 
#     break_even:dict=None, 
#     cost_structure:dict=None,
#     pnl_table: list[dict]=None

#     ):
#     with ui.grid(columns=1).classes('w-full gap-4 mt-2'):
#         if pnl_table is not None:
#             render_pnl_table(pnl_table)
#         if cash_flow_history is not None:
#             render_cashflow_chart(cash_flow_history)
#         if break_even is not None:
#             render_break_even_chart(break_even)
#         if cost_structure is not None:
#             render_cost_structure_chart(cost_structure)
def render_finance_charts(
    cash_flow_history: list[dict] = None,
    break_even: dict = None,
    cost_structure: dict = None,
    pnl_table: list[dict] = None,
):
    with ui.grid().classes(
        'w-full grid-cols-1 lg:grid-cols-3 gap-4 mt-2'
    ):
        if pnl_table is not None:
            # 'w-full min-w-0'
            # lg:col-span-2 min-w-0
            with ui.element('div').classes('w-full min-w-0'):
                render_pnl_table(pnl_table)

        if cost_structure is not None:
            with ui.element('div').classes('lg:col-span-1 min-w-0'):
                render_cost_structure_chart(cost_structure)

        if cash_flow_history is not None:
            with ui.element('div').classes('lg:col-span-2 min-w-0'):
                render_cashflow_chart(cash_flow_history)

        if break_even is not None:
            with ui.element('div').classes('lg:col-span-1 min-w-0'):
                render_break_even_chart(break_even)