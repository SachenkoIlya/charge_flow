from nicegui import ui

from frontend.features.trends.components import (
    render_ui_echart,
    render_midle_right, 
)
mock_metrics = [
    {
        'label': 'Текущий год',
        'value': '93 000',
        'suffix': 'кВт⋅ч',
    },
    {
        'label': 'Прошлый год',
        'value': '80 000',
        'suffix': 'кВт⋅ч',
    },
    {
        'label': 'Рост YoY',
        'value': '12',
        'suffix': '%',
        'emoji': '↗',
        'color': 'text-green-500',
    },
]


def render_midle_block(metrics: dict = None):
    if not metrics:
        metrics = mock_metrics
    with ui.element('div').classes(
        'flex-[2] min-w-0 h-full rounded-lg p-2 overflow-hidden'
    ):
        render_ui_echart()
    with ui.column().classes(
        'flex-[1] gap-2 h-full overflow-hidden'
    ):
        render_midle_right(metrics)


async def render_middle():
    with ui.row().classes('w-full gap-2 items-stretch h-[260px]'):
        # левый блок
        with ui.element('div').classes(
            'flex-1 h-full bg-white rounded-xl shadow-sm border border-gray-200 p-3 overflow-hidden'
        ):
            ui.label('ЭНЕРГИЯ').classes('text-sm')
            with ui.row().classes('w-full h-[210px] gap-2 mt-1 items-stretch'):
                render_midle_block()
        # правый блок
        with ui.element('div').classes(
            'flex-1 h-full bg-white rounded-xl shadow-sm border border-gray-200 p-3 overflow-hidden'
        ):
            with ui.row().classes('w-full items-center justify-between mb-1'):
                ui.label('ДИНАМИКА ПО ДНЯМ').classes('text-sm font-semibold')

            with ui.element('div').classes('w-full h-[210px]'):
                render_ui_echart()