from nicegui import ui

from frontend.components.chart_card import chart_card
from core.logger.logger import logger

def render_cost_structure_chart(cost_structure:dict):
    chart = prepare_charts(cost_structure)
    logger.debug(chart)
    with chart_card():
        ui.label('Структура затрат').classes('text-sm font-bold mb-2')
        ui.echart(chart).classes('w-full h-[220px]')

def prepar_charts_v2(data: dict):
    
    res = [
        {'name': k, 'value': v}
        for k,v in data.items()
    ] 

    return {
    'tooltip': {
        'trigger': 'item',
        'formatter': '{b}<br/>Оборот: {c} ₽ ({d}%)'
    },
    'series': [
        {
            'name': 'Оборот',
            'type': 'pie',
            'radius': '80%',

            'data': res,

            'emphasis': {
                'itemStyle': {
                    'shadowBlur': 10,
                    'shadowOffsetX': 0,
                    'shadowColor': 'rgba(0, 0, 0, 0.3)'
                }
            }
        }
    ]
}
# def prepar_charts(cost_structure: dict):
#     return {
#         'backgroundColor': 'transparent',
#         'tooltip': {'trigger': 'item'},
#         # 'legend': {
#         #     'orient': 'vertical',
#         #     'right': 10,
#         #     'top': 'middle',
#         #     'textStyle': {'color': '#9ca3af'},
#         # },
#         'series': [
#             {
#                 'name': 'opex расходы',
#                 'type': 'pie',
#                 'radius': ['55%', '85%'],
#                 'center': ['50%', '50%'],
#                 'avoidLabelOverlap': True,
#                 'label': {'show': False},
#                 'data': [
#                     {'value': cost_structure['electricity_compensation'], 'name': 'Затраты на эл/энергию'},
#                     {'value': cost_structure['rent_payment'], 'name': 'Аренда'},
#                     {'value': cost_structure['operator_commission'], 'name': 'Комиссия оператора'},
#                     {'value': cost_structure['service_maintenance'], 'name': 'Сервисное обслуживание'},
#                     {'value': cost_structure['internet_and_connection'], 'name': 'Интернет'},
#                     {'value': cost_structure['taxes'], 'name': 'Налоги'},
#                 ],
#             }
#         ],
#     }
def prepare_charts(cost_structure: dict):
    data = [
        {'value': cost_structure['electricity_compensation'], 'name': 'Электроэнергия'},
        {'value': cost_structure['rent_payment'], 'name': 'Аренда'},
        {'value': cost_structure['operator_commission'], 'name': 'Комиссия оператора'},
        {'value': cost_structure['service_maintenance'], 'name': 'Сервис'},
        {'value': cost_structure['internet_and_connection'], 'name': 'Интернет'},
        {'value': cost_structure['taxes'], 'name': 'Налоги'},
    ]

    # убрать нулевые статьи
    data = [x for x in data if x['value'] > 0]

    # сортировка по величине
    data = sorted(data, key=lambda x: x['value'], reverse=True)

    return {
        'backgroundColor': 'transparent',

        'tooltip': {
            'trigger': 'item',
            'formatter': (
                '{b}<br/>'
                'Сумма: {c} ₽<br/>'
                'Доля: {d}%'
            )
        },

        'legend': {
            'type': 'scroll',
            'orient': 'vertical',
            'right': 10,
            'top': 'middle',
        },

        'series': [
            {
                'name': 'OPEX',
                'type': 'pie',
                'radius': ['45%', '75%'],
                'center': ['40%', '50%'],

                'selectedMode': 'multiple',

                'data': data,

                'label': {
                    'show': True,
                    'formatter': '{b}\n{d}%'
                },

                'emphasis': {
                    'scale': True,
                    'scaleSize': 10,
                    'itemStyle': {
                        'shadowBlur': 15,
                        'shadowColor': 'rgba(0,0,0,0.3)'
                    }
                },

                'itemStyle': {
                    'borderRadius': 5,
                    'borderColor': '#fff',
                    'borderWidth': 2
                }
            }
        ]
    }