
def get_pie_charts_options(data:list[dict]):
    return  {
        # 'tooltip': {
        #     'trigger': 'item',
        #     'formatter': '{b}: {c} ₽ ({d}%)', 
        # },
        'tooltip': {
            'trigger': 'item',
            ':formatter': """
                function(params) {
                    return params.name + ': ' +
                        params.value.toLocaleString('ru-RU') + ' ₽ (' +
                        params.percent + '%)';
                }
                """
        },
        'legend': {
            'selectedMode': False,
            'orient': 'vertical',
            'right': 10,
            'top': 5
        },

        # 'color': ['#1976D2', '#42A5F5', '#64B5F6', '#90CAF9', '#BBDEFB', '#E3F2FD'],
        'color': [
            '#6366F1',  # indigo
            '#8B5CF6',  # purple
            "#F13090",  # pink
            '#F59E0B',  # amber
            '#10B981',  # emerald
            '#6B7280',  # gray
        ],
        'series': [
            {
                'name': 'Локация',
                'type': 'pie',
                'radius': ['60%', '80%'],
                'center': ['35%', '50%'],
                'itemStyle': {
                    'borderRadius': 10,
                    'borderColor': '#fff',
                    'borderWidth': 15
                },

                'label': {
                    'show': True,
                    'position': 'center',
                    'formatter': 'Оборот по локациям',
                    'fontSize': 16,
                    'fontWeight': 'bold'
                    },

                'labelLine': {
                    'show': False
                },

                'data': data
            }
        ]
    }

def get_pie_charts_options_v2(data: list[dict]):
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