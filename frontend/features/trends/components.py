from nicegui import ui  
from frontend.features.trends.charts import (
    render_connector_types_chart, 
    render_revenue_chart, 
    render_daily_dynamics_chart, 
    render_sessions_chart
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

def get_metrics(metric: dict):
    label = metric.get('label', '')
    value = metric.get('value', '')
    suffix = metric.get('suffix', '')
    emoji = metric.get('emoji', '')
    color = metric.get('color', 'text-gray-900')

    text = f'{value} {suffix}'.strip()
    if emoji:
        text = f'{text} {emoji}'

    with ui.element('div').classes(
        'w-full bg-white rounded-lg shadow-sm border border-gray-200 p-3'
    ):
        ui.label(label).classes('text-xs text-gray-500')
        ui.label(text).classes(f'text-lg font-bold {color}')

def render_high_block(metrics: dict=None):
    if not metrics:
        metrics = mock_metrics_1
    with ui.element('div').classes(
        'flex-[4] min-w-0 border-2 border-blue-400 rounded-lg p-4'
        ):
        render_revenue_left()
    
    with ui.element('div').classes(
        'flex-[1] border-2 border-green-400 rounded-lg p-4'
    ):
        render_revenue_right(metrics)


def render_revenue_left():
    options = render_revenue_chart()
    ui.echart(options).classes('w-full h-[240px]')

def render_revenue_right(metrics):
    with ui.column().classes('flex-[1] gap-3 h-full justify-between'):
        for metric in metrics:
            get_metrics(metric)
           



def render_midle_block(metrics:dict):
    if not metrics:
        metrics = mock_metrics
    with ui.element('div').classes(
        'flex-[2] min-w-0 border-2 border-blue-400 rounded-lg p-3'
    ):
        render_midle_left()
    with ui.column().classes(
        'flex-[1] gap-3 h-full justify-between'
    ):
        render_midle_right(metrics)


def render_midle_left():
    options = render_revenue_chart()
    ui.echart(options).classes('w-full h-[220px]')

def render_midle_right(metrics:dict=None):
    for metric in metrics:
        get_metrics(metric)


def dynamics_by_day_from_middle_render():
    options = render_daily_dynamics_chart()
    ui.echart(options).classes('w-full h-[240px]')