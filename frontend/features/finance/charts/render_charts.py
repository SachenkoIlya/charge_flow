from nicegui import ui

from frontend.features.finance.charts.cashflow import render_cashflow_chart
from frontend.features.finance.charts.break_even import render_break_even_chart
from frontend.features.finance.charts.cost_structure import render_cost_structure_chart


def render_finance_charts(cash_flow_history :list[dict], break_even:dict, cost_structure:dict):
    with ui.grid(columns=3).classes('w-full gap-4 mt-4'):
        render_cashflow_chart(cash_flow_history)
        render_break_even_chart(break_even)
        render_cost_structure_chart(cost_structure)
        