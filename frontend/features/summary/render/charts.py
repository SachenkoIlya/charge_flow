from nicegui import ui

def render_chart(metrics:dict):



    with ui.card().classes(
        '''
        w-full
        mt-5
        bg-[#101923]/90
        border border-[#1f2937]
        rounded-xl
        shadow-xl
        p-4
        '''
    ):

        ui.label('Динамика ключевых метрик').classes(
            'text-base font-bold text-white mb-2'
        )

        ui.echart(metrics).classes(
            'w-full h-[250px]'
        )

CHART_METRICS = {
        'backgroundColor': 'transparent',

        'tooltip': {
            'trigger': 'axis',
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
            'data': [
                '1 май', '3 май', '5 май', '7 май', '9 май',
                '11 май', '13 май', '15 май', '17 май',
                '19 май', '21 май', '23 май', '25 май',
                '27 май', '29 май', '31 май'
            ],
            'axisLine': {
                'lineStyle': {'color': '#374151'}
            },
            'axisLabel': {
                'color': '#9ca3af'
            }
        },

        'yAxis': {
            'type': 'value',
            'axisLine': {
                'lineStyle': {'color': '#374151'}
            },
            'splitLine': {
                'lineStyle': {'color': '#1f2937'}
            },
            'axisLabel': {
                'color': '#9ca3af'
            }
        },

        'series': [
            {
                'name': 'Выручка',
                'type': 'line',
                'smooth': True,
                'data': [3.8, 4.2, 2.4, 3.3, 3.5, 3.0, 3.8, 3.2, 2.8, 3.9, 3.6, 3.1, 4.1, 3.5, 3.2, 3.9],
                'lineStyle': {'width': 3},
                'symbolSize': 8,
                'color': '#22c55e',
            },
            {
                'name': 'Сессии',
                'type': 'line',
                'smooth': True,
                'data': [2.9, 3.3, 1.6, 2.5, 2.6, 2.2, 2.8, 2.3, 2.1, 2.9, 2.7, 2.3, 3.1, 2.5, 2.2, 2.9],
                'lineStyle': {'width': 3},
                'symbolSize': 8,
                'color': '#3b82f6',
            },
            {
                'name': 'Загрузка',
                'type': 'line',
                'smooth': True,
                'data': [1.8, 2.2, 0.9, 1.4, 1.5, 1.2, 1.6, 1.3, 1.1, 1.7, 1.5, 1.2, 1.9, 1.5, 1.3, 1.8],
                'lineStyle': {'width': 3},
                'symbolSize': 8,
                'color': '#a855f7',
            },
        ]
    }