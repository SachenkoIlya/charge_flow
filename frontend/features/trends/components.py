from nicegui import ui  
from core.logger.logger import make_logger
from frontend.components.metrics import get_metrics
from frontend.features.trends.charts import (
    render_connector_types_chart, 
    render_revenue_chart, 
    render_daily_dynamics_chart, 
    render_sessions_chart
)

logger = make_logger(__name__, use_telegram=False)





def render_revenue_left():
    options = render_revenue_chart()
    ui.echart(options).classes('w-full h-full')

def render_revenue_right(metrics):
    with ui.column().classes('flex-[1] gap-2 h-full overflow-hidden'):
        for metric in metrics:
            get_metrics(metric)
           




def render_ui_echart(options:dict=None):
    if not options:
        options = render_revenue_chart()
    ui.echart(options).classes('w-full h-full')

def render_midle_right(metrics:dict=None):
    for metric in metrics:
        get_metrics(metric)





mock_3 = [
    {
        'title': 'Доступность', 
        'value': '98%', 
        'color': 'text-green-500',
        'border': 'border-green-500',
    },  
    {
        'title': 'Простой', 
        'value': '2%', 
        'color': 'text-red-500',
        'border': 'border-red-500',
    },
    {
        'title': 'Утилизация', 
        'value': '67%', 
        'color': 'text-gray-700',
        'border': 'border-purple-500',
    },
    {
        'title': 'Время работы',
        'value': '67%', 
        'color': 'text-gray-700',
        'border': 'border-blue-500',
    }
]

mock_4 = [
    {
        'title':'Текущий', 
        'value':'120', 
        'delta':'+8%',
        'color': None
    },  
    {
        'title':'-1 период', 
        'value':'98%', 
        'delta':'+8%',
        'color': None
    },
    {
        'title':'-2 период', 
        'value':'87', 
        'delta': None,
        'color': None
    },
] 

def render_visual_container(label: str, metrics: list[dict[str, str]]=None, CARD:str=None, STYLE_LABEL:str=None) -> None:

    if not metrics:
        if label == 'СРЕДНЕЕ':
            metrics = mock_4
        if label == 'ЭКСПЛУАТАЦИЯ':
            metrics = mock_3
   
    with ui.element('div').classes(CARD):
        ui.label(label).classes(STYLE_LABEL)
        with ui.row().classes('w-full gap-2 items-start'):
            for m in metrics:
                render_small_metric(
                    title=m.get('title'),
                    value=m.get('value'),
                    delta=m.get('delta'),
                    color=m.get('color'),
                    border=m.get('border'),
                )


METRIC_CARD_CLASSES = (
    'flex-1 min-w-0 h-[72px] '
    'bg-white rounded-lg shadow-sm border p-2 '
    'flex flex-col justify-center overflow-hidden'
)

def render_small_metric(title, value, delta='', color='', border=''):
    with ui.element('div').classes(
        f'{METRIC_CARD_CLASSES} border-b-2 {border}'
    ):
        ui.label(title).classes('text-xs text-gray-500 leading-tight')
        ui.label(value).classes(f'text-base font-bold leading-tight {color}')
        if delta:
            ui.label(delta).classes('text-xs text-green-500')