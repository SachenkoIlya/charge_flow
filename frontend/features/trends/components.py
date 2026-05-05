from nicegui import ui  
from core.logger.logger import make_logger
from frontend.features.trends.charts import (
    render_connector_types_chart, 
    render_revenue_chart, 
    render_daily_dynamics_chart, 
    render_sessions_chart
)

logger = make_logger(__name__, use_telegram=False)
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
        'w-full flex-1 min-h-0 bg-white rounded-lg shadow-sm border border-gray-200 p-2 overflow-hidden'
    ):
        ui.label(label).classes('text-xs text-gray-500 leading-tight')
        ui.label(text).classes(f'text-base font-bold leading-tight {color}')


def render_high_block(metrics: dict = None):
    if not metrics:
        metrics = mock_metrics_1
    with ui.element('div').classes(
        'flex-[4] min-w-0 h-full border-2 border-blue-400 rounded-lg p-2 overflow-hidden'
    ):
        render_revenue_left()
    
    with ui.element('div').classes(
        'flex-[1] h-full border-2 border-green-400 rounded-lg p-2 overflow-hidden'
    ):
        render_revenue_right(metrics)

def render_revenue_left():
    options = render_revenue_chart()
    ui.echart(options).classes('w-full h-full')

def render_revenue_right(metrics):
    with ui.column().classes('flex-[1] gap-2 h-full overflow-hidden'):
        for metric in metrics:
            get_metrics(metric)
           



def render_midle_block(metrics: dict = None):
    if not metrics:
        metrics = mock_metrics

    with ui.element('div').classes(
        'flex-[2] min-w-0 h-full border-2 border-blue-400 rounded-lg p-2 overflow-hidden'
    ):
        render_midle_left()

    with ui.column().classes(
        'flex-[1] gap-2 h-full overflow-hidden'
    ):
        render_midle_right(metrics)


def render_midle_left():
    options = render_revenue_chart()
    ui.echart(options).classes('w-full h-full')

def render_midle_right(metrics:dict=None):
    for metric in metrics:
        get_metrics(metric)


def dynamics_by_day_from_middle_render():
    options = render_daily_dynamics_chart()
    ui.echart(options).classes('w-full h-full')



mock_3 = [
    {
        'title':'Доступность', 
        'value':'98%', 
        'color':'text-green-500',
    },  
    {
        'title':'Простой', 
        'value':'2%', 
        'color':'text-red-500',
    },
    {
        'title':'Утилизация', 
        'value':'67%', 
        'color':'text-gray-700',
    },
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
        with ui.row().classes('w-full gap-2'):
            for m in metrics:
                render_small_metric(
                    title=m.get('title'),
                    value=m.get('value'),
                    delta=m.get('delta'),
                    color=m.get('color'),
                )


METRIC_CARD_CLASSES = (
    'flex-1 min-w-0 h-full '
    'bg-white rounded-lg shadow-sm border border-gray-200 p-2 overflow-hidden'
)

def render_small_metric(title, value, delta='', color=''):
    with ui.element('div').classes(METRIC_CARD_CLASSES):
        ui.label(title).classes('text-xs text-gray-500 leading-tight')
        ui.label(value).classes(f'text-base font-bold leading-tight {color}')
        if delta:
            ui.label(delta).classes('text-xs text-green-500')
    

