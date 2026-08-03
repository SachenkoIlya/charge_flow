from nicegui import ui

from frontend.components.chart_card import chart_card


def render_cost_structure_chart(cost_structure:dict):
    chart = prepar_charts(cost_structure)
    with chart_card():
        ui.label('Структура затрат opex').classes('text-sm font-bold mb-2')
        ui.echart(chart).style(
            'height: 300px; width: 100%;'
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
    total = sum(d['value'] for d in data)

    formatted_total = f'{total:,.0f}'.replace(',', ' ')

    return {
        'backgroundColor': 'transparent',

        'tooltip': {
            'trigger': 'item',
            'formatter': (
                '<b>{b}</b><br/>'
                'Сумма: {c} ₽<br/>'
                'Доля: {d}%'
            ),
        },

        'graphic': [
            {
                'type': 'text',
                'left': 'center',
                'top': '43%',
                'silent': True,
                'style': {
                    'text': f'{formatted_total} ₽',
                    'fill': '#ffffff',
                    'fontSize': 22,
                    'fontWeight': 700,
                    'textAlign': 'center',
                },
            },
            {
                'type': 'text',
                'left': 'center',
                'top': '54%',
                'silent': True,
                'style': {
                    'fill': '#9ca3af',
                    'fontSize': 13,
                    'fontWeight': 500,
                    'textAlign': 'center',
                },
            },
        ],

        'series': [
            {
                'name': 'OPEX расходы',
                'type': 'pie',

                'radius': ['65%', '95%'],
                'center': ['50%', '52%'],

                'label': {
                    'show': False,
                },

                'labelLine': {
                    'show': False,
                },

                'data': data,

                'emphasis': {
                    'scale': True,
                    'scaleSize': 10,
                    'itemStyle': {
                        'shadowBlur': 20,
                        'shadowOffsetX': 0,
                        'shadowColor': 'rgba(0, 0, 0, 0.25)',
                    },
                },

                'itemStyle': {
                    'borderRadius': 5,
                    'borderColor': '#101923',
                    'borderWidth': 2,
                },

                'selectedMode': 'single',
            },
        ],
    }