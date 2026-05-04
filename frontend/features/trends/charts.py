def render_revenue_chart():
    options = {
        'tooltip': {'trigger': 'axis'},
        'legend': {
            'bottom': 0,
            'data': ['Текущий год', 'Прошлый год'],
        },
        'grid': {
            'left': 45,
            'right': 20,
            'top': 30,
            'bottom': 45,
        },
        'xAxis': {
            'type': 'category',
            'data': ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'],
        },
        'yAxis': {
            'type': 'value',
            'axisLabel': {'formatter': '{value}k'},
        },
        'series': [
            {
                'name': 'Текущий год',
                'type': 'line',
                'smooth': True,
                'data': [135, 142, 160, 144, 153, 149, 147, 136, 152, 158, 172, 169],
            },
            {
                'name': 'Прошлый год',
                'type': 'line',
                'smooth': True,
                'data': [78, 82, 96, 87, 96, 94, 90, 74, 89, 91, 107, 101],
            },
        ],
    }
    return options
    