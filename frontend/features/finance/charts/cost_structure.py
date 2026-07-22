from nicegui import ui

from frontend.components.chart_card import chart_card


def render_cost_structure_chart(cost_structure:dict):
    chart = prepar_charts_v2([cost_structure])
    with chart_card():
        ui.label('Структура затрат').classes('text-sm font-bold mb-2')
        ui.echart(chart).classes('w-full h-[220px]')

def prepar_charts_v2(data: list[dict]):
    return {
    # 'title': {
    #     'text': 'Оборот по локациям',
    #     'left': 'center',
    # },

    'tooltip': {
        'trigger': 'item',
        'formatter': '{b}<br/>Оборот: {c} ₽ ({d}%)'
    },

    # 'legend': {
    #     'orient': 'vertical',
    #     'left': 'right'
    # },

    'series': [
        {
            'name': 'Оборот',
            'type': 'pie',
            'radius': '80%',

            'data': data,

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
def prepar_charts(cost_structure: dict):
    return {
        'backgroundColor': 'transparent',
        'tooltip': {'trigger': 'item'},
        # 'legend': {
        #     'orient': 'vertical',
        #     'right': 10,
        #     'top': 'middle',
        #     'textStyle': {'color': '#9ca3af'},
        # },
        'series': [
            {
                'name': 'opex расходы',
                'type': 'pie',
                'radius': ['55%', '85%'],
                'center': ['50%', '50%'],
                'avoidLabelOverlap': True,
                'label': {'show': False},
                'data': [
                    {'value': cost_structure['electricity_compensation'], 'name': 'Затраты на эл/энергию'},
                    {'value': cost_structure['rent_payment'], 'name': 'Аренда'},
                    {'value': cost_structure['operator_commission'], 'name': 'Комиссия оператора'},
                    {'value': cost_structure['service_maintenance'], 'name': 'Сервисное обслуживание'},
                    {'value': cost_structure['internet_and_connection'], 'name': 'Интернет'},
                    {'value': cost_structure['taxes'], 'name': 'Налоги'},
                ],
            }
        ],
    }