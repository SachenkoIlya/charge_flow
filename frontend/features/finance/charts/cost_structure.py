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

    return {
        'backgroundColor': 'transparent',

        'tooltip': {
            'trigger': 'item',
            
            'formatter': (
                '<b>{b}</b><br/>'
                'Сумма: {c} ₽<br/>'
                'Доля: {d}%'
            ).replace('{c}', '{c}')
        },

        # 'legend': {
        #     'show': True,
        #     'orient': 'vertical',
        #     'right': 5,            # Увеличили отступ от края, чтобы текст не прижимался
        #     'top': 15,
        #     'selectedMode': False,
            
        #     # 1. Делаем цветные квадратики больше (было 12)
        #     'itemWidth': 18,        
        #     'itemHeight': 18,       
        #     'itemGap': 15,          # Добавили расстояние МЕЖДУ строками легенды, чтобы они не слипались
            
        #     'textStyle': {
        #         'color': '#9ca3af',
        #         'fontSize': 14,     # 2. Увеличили размер шрифта текста (дефолт обычно 12)
        #         'fontWeight': '500' # Сделали текст чуть плотнее, чтобы лучше читался
        #     }
        # },

        'series': [
            {
                'name': 'OPEX расходы',
                'type': 'pie',

                'radius': ['50%', '90%'],
                'center': ['50%', '50%'],

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