from nicegui import ui

from frontend.components.pnl_table import render_pnl_table
from frontend.features.finance.charts.cashflow import render_cashflow_chart
from frontend.features.finance.charts.break_even import render_break_even_chart
from frontend.features.finance.charts.cost_structure import render_cost_structure_chart


def render_finance_charts(
    cash_flow_history :list[dict]=None, 
    break_even:dict=None, 
    cost_structure:dict=None,
    pnl_table: list[dict]=None

    ):
    with ui.grid(columns=1).classes('w-full gap-4 mt-2'):
        if pnl_table is not None:
            render_pnl_table(pnl_table)
        if cash_flow_history is not None:
            render_cashflow_chart(cash_flow_history)
        if break_even is not None:
            render_break_even_chart(break_even)
        if cost_structure is not None:
            render_cost_structure_chart(cost_structure)
        