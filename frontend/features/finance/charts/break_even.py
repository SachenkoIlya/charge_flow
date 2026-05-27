
from nicegui import ui

from frontend.components.chart_card import chart_card


def render_break_even_chart(break_even):
    with chart_card():
        ui.label('График безубыточности').classes('text-sm font-bold mb-2')
        ui.echart(break_even).classes('w-full h-[220px]')



BREAK_EVEN_METRICS = {
        'backgroundColor': 'transparent',
        'tooltip': {'trigger': 'axis'},
        'legend': {
            'top': 0,
            'textStyle': {'color': '#9ca3af'},
        },
        'grid': {'left': '8%', 'right': '5%', 'top': '18%', 'bottom': '14%'},
        'xAxis': {
            'type': 'category',
            'data': ['0', '200K', '400K', '600K', '800K', '1M', '1.2M', '1.4M'],
            'axisLabel': {'color': '#9ca3af'},
            'axisLine': {'lineStyle': {'color': '#374151'}},
        },
        'yAxis': {
            'type': 'value',
            'axisLabel': {'color': '#9ca3af', 'formatter': '{value}M'},
            'splitLine': {'lineStyle': {'color': '#1f2937'}},
        },
        'series': [
            {'name': 'Выручка', 'type': 'line', 'data': [0.05, 0.3, 0.55, 0.8, 1.0, 1.2, 1.38, 1.55], 'color': '#22c55e'},
            {'name': 'Переменные затраты', 'type': 'line', 'data': [0.3, 0.38, 0.48, 0.62, 0.78, 0.9, 1.05, 1.2], 'color': '#3b82f6'},
            {'name': 'Постоянные затраты', 'type': 'line', 'data': [0.25, 0.3, 0.35, 0.39, 0.43, 0.48, 0.52, 0.56], 'color': '#a855f7'},
            {
                'name': 'Точка безубыточности',
                'type': 'line',
                'markLine': {
                    'symbol': 'none',
                    'lineStyle': {'color': '#f59e0b', 'type': 'dashed'},
                    'data': [{'xAxis': '800K'}],
                },
                'data': [],
            },
        ],
    }
