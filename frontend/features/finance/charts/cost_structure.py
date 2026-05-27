from nicegui import ui

from frontend.components.chart_card import chart_card


def render_cost_structure_chart(cost_structure:dict):
    with chart_card():
        ui.label('Структура затрат').classes('text-sm font-bold mb-2')
        ui.echart(cost_structure).classes('w-full h-[220px]')


COST_STRUCTURE = {
        'backgroundColor': 'transparent',
        'tooltip': {'trigger': 'item'},
        'legend': {
            'orient': 'vertical',
            'right': 10,
            'top': 'middle',
            'textStyle': {'color': '#9ca3af'},
        },
        'series': [
            {
                'name': 'Структура затрат',
                'type': 'pie',
                'radius': ['45%', '72%'],
                'center': ['32%', '55%'],
                'avoidLabelOverlap': True,
                'label': {'show': False},
                'data': [
                    {'value': 10.25, 'name': 'Затраты на эл/энергию'},
                    {'value': 4.09, 'name': 'Аренда'},
                    {'value': 2.57, 'name': 'Комиссия оператора'},
                    {'value': 1.98, 'name': 'Сервисное обслуживание'},
                    {'value': 0.71, 'name': 'Интернет'},
                    {'value': 1.23, 'name': 'Налоги'},
                ],
            }
        ],
    }