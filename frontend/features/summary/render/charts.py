from nicegui import ui
from core.logger.logger import logger


def render_chart(data:dict):
    metrics = get_chart_metrics(data)

    with ui.card().classes(
        '''
        w-full
        bg-[#101923]/90
        border border-[#1f2937]
        rounded-xl
        shadow-xl
        px-4 pt-3 pb-1
        '''
    ):

        ui.label('Динамика ключевых метрик').classes(
            'text-base font-bold text-white mb-2'
        )

        ui.echart(metrics).classes(
              'w-full h-[400px]'
        )


def get_chart_metrics(data:dict):
    charts = data['requested_metrics']['charts']
    x_axis = charts['xAxis']
    series = charts['series']
    logger.debug(f'x_axis len={len(x_axis)}: {x_axis}')
    logger.debug(f'revenue len={len(series["revenue"])}: {series["revenue"]}')
    logger.debug(f'sessions len={len(series["sessions"])}: {series["sessions"]}')
    logger.debug(f'utilisation len={len(series["utilisation"])}: {series["utilisation"]}')
    
    return {
            'backgroundColor': 'transparent',

           'tooltip': {
                'trigger': 'axis',
                'triggerOn': 'click',
            },

            'legend': {
                'top': 0,
                'textStyle': {
                    'color': '#9ca3af',
                }
            },

            'grid': {
                'left': '3%',
                'right': '4%',
                'bottom': '3%',
                'containLabel': True
            },

            'xAxis': {
                'type': 'category',
                'boundaryGap': False,
                'data': x_axis,
                'axisLine': {
                    'lineStyle': {'color': '#374151'}
                },
                'axisLabel': {
                    'color': '#9ca3af'
                }
            },

            "yAxis": [
                {
                    "type": "value",
                    "name": "₽",
                    "position": "left",
                    "axisLabel": {"color": "#9ca3af"},
                    "splitLine": {"lineStyle": {"color": "#1f2937"}},
                },
                {
                    "type": "value",
                    "name": "% / шт",
                    "position": "right",
                    "axisLabel": {"color": "#9ca3af"},
                    "splitLine": {"show": False},
                },
            ],

            'series': [
                {
                    "name": "Выручка",
                    "type": "line",
                    "smooth": True,
                    "data": series["revenue"],
                    "yAxisIndex": 0,
                    "lineStyle": {"width": 3},
                    'showSymbol': True,
                    "symbolSize": 10,
                    "color": "#22c55e",
                },
                {
                    "name": "Сессии",
                    "type": "line",
                    "smooth": True,
                    "data": series["sessions"],
                    "yAxisIndex": 1,
                    "lineStyle": {"width": 3},
                    'showSymbol': True,
                    "symbolSize": 10,
                    "color": "#3b82f6",
                },
                {
                    "name": "Загрузка",
                    "type": "line",
                    "smooth": True,
                    "data": series["utilisation"],
                    "yAxisIndex": 1,
                    "lineStyle": {"width": 3},
                    'showSymbol': True,
                    "symbolSize": 10,
                    "color": "#a855f7",
                },
            ]
        }

     