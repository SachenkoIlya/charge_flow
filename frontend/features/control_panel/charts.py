from nicegui import ui
from frontend.features.control_panel.config import get_pie_charts_options

def render_pie_chart(data: list[dict]):
    with ui.column().classes('flex-2'):
        # outline outline-2 outline-red-500
        ui.echart(get_pie_charts_options(data=data)).classes('w-full h-100')