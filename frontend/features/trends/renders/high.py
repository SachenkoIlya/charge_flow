from frontend.features.trends.components import (
    render_ui_echart, 
    render_revenue_right
)
from nicegui import ui

mock_metrics_1 = [
    {
        'label': 'Текущий год',
        'value': '1 863 000',
        'suffix': 'р',
    },
    {
        'label': 'Прошлый год',
        'value': '1 540 000',
        'suffix': 'р',
    },
    {
        'label': 'Рост YoY',
        'value': '12',
        'suffix': '%',
        'emoji': '↗',
        'color': 'text-green-500',
    },
]


def render_high_block(metrics: dict = None):
    if not metrics:
        metrics = mock_metrics_1
    with ui.element('div').classes(
        'flex-[4] min-w-0 h-full rounded-lg p-2 overflow-hidden'
    ):
        render_ui_echart()
    
    with ui.element('div').classes(
        'flex-[1] h-full p-2 overflow-hidden'
    ):
        render_revenue_right(metrics)



async def render_high():
    with ui.element('div').classes(
        'w-full h-[300px] bg-white rounded-xl shadow-sm border border-gray-200 p-3 overflow-hidden'
    ):
        ui.label('REVENUE BLOCK').classes('text-sm')

        with ui.element('div').classes(
            'flex w-full h-[250px] gap-2 mt-1 items-stretch'
        ):
            render_high_block()