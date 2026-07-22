from nicegui import ui

from frontend.components.chart_card import chart_card


def render_cost_structure_chart(cost_structure:dict):
    chart = prepar_charts(cost_structure)
    with chart_card():
        ui.label('Структура затрат').classes('text-sm font-bold mb-2')
        ui.echart(chart).style(
            'height: 220px; width: 100%;'
        )


def prepar_charts(cost_structure: dict):
    data = [
        {'value': cost_structure['electricity_compensation'], 'name': 'Электроэнергия'},
        {'value': cost_structure['rent_payment'], 'name': 'Аренда'},
        {'value': cost_structure['operator_commission'], 'name': 'Комиссия оператора'},
        {'value': cost_structure['service_maintenance'], 'name': 'Сервисное обслуживание'},
        {'value': cost_structure['internet_and_connection'], 'name': 'Интернет'},
        {'value': cost_structure['taxes'], 'name': 'Налоги'},
    ]

    data = [x for x in data if x['value'] > 0]

    return {
        'backgroundColor': 'transparent',

        'tooltip': {
            'trigger': 'item',
            'formatter': (
                '<b>{b}</b><br/>'
                'Сумма: {c} ₽<br/>'
                'Доля: {d}%'
            )
        },

        'legend': {
            'show': True,
            'orient': 'vertical',
            'right': 10,
            'top': 'center',
            'itemWidth': 12,
            'itemHeight': 12
        },

        'series': [
            {
                'name': 'OPEX расходы',
                'type': 'pie',

                'radius': ['55%', '80%'],
                'center': ['40%', '50%'],

                # подписи скрыты
                'label': {
                    'show': False
                },

                'labelLine': {
                    'show': False
                },

                'data': data,

                # красивый hover
                'emphasis': {
                    'scale': True,
                    'scaleSize': 10,

                    'itemStyle': {
                        'shadowBlur': 20,
                        'shadowOffsetX': 0,
                        'shadowColor': 'rgba(0,0,0,0.25)'
                    }
                },

                'itemStyle': {
                    'borderRadius': 5,
                    'borderColor': '#fff',
                    'borderWidth': 2
                },

                # клик по сектору
                'selectedMode': 'single'
            }
        ]
    }