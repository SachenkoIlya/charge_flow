from nicegui import ui

from frontend.features.finance.charts.cashflow import render_cashflow_chart

def render_finance_charts(cashflow):
    with ui.grid(columns=3).classes('w-full gap-4 mt-5'):
        render_cashflow_chart(cashflow)
        # render_break_even_chart()
        # render_cost_structure_chart()
        ...