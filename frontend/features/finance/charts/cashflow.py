from frontend.components.chart_card import chart_card
from nicegui import ui


def render_cashflow_chart(metrics):
    with chart_card('Накопленный денежный поток'):
        ui.label('Накопленный денежный поток').classes('text-sm font-bold mb-2')
        ui.echart(metrics).classes('w-full h-[220px]')



CASHFLOW_METRICS = {
        'backgroundColor': 'transparent',
        'tooltip': {'trigger': 'axis'},
        'grid': {
            'left': '8%',
            'right': '5%',
            'top': '18%',
            'bottom': '12%',
        },
        'xAxis': {
            'type': 'category',
            'data': ['Дек 2024', 'Янв 2025', 'Фев 2025', 'Мар 2025', 'Апр 2025', 'Май 2025'],
            'axisLabel': {'color': '#9ca3af'},
            'axisLine': {'lineStyle': {'color': '#374151'}},
        },
        'yAxis': {
            'type': 'value',
            'axisLabel': {'color': '#9ca3af'},
            'splitLine': {'lineStyle': {'color': '#1f2937'}},
        },
        'series': [{
            'name': 'Cash flow',
            'type': 'line',
            'smooth': True,
            'data': [-30, -18, -7, 2, 12, 28.9],
            'color': '#22c55e',
            'symbolSize': 7,
            'lineStyle': {'width': 3},
            'areaStyle': {'opacity': 0.08},
        }],
    }