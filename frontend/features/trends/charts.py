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
    




def render_daily_dynamics_chart():
    return {
        'tooltip': {'trigger': 'axis'},
        'legend': {
            'bottom': 0,
            'data': ['Текущий месяц', 'Прошлый месяц', 'Позапрошлый месяц'],
        },
        'grid': {
            'left': 45,
            'right': 20,
            'top': 30,
            'bottom': 45,
        },
        'xAxis': {
            'type': 'category',
            'data': [str(i) for i in range(1, 32)],
        },
        'yAxis': {
            'type': 'value',
            'axisLabel': {'formatter': '{value}k'},
        },
        'series': [
            {
                'name': 'Текущий месяц',
                'type': 'line',
                'smooth': True,
                'data': [6.8, 6.5, 5.1, 3.7, 4.8, 3.6, 3.9, 5.9, 6.0, 6.1, 5.8, 4.9, 3.7, 4.6, 4.2, 5.0, 5.5, 6.3, 4.8, 4.3, 4.0, 4.2, 5.0, 4.4, 4.3, 6.5, 6.4, 3.9, 4.2, 5.7, 6.3],
            },
            {
                'name': 'Прошлый месяц',
                'type': 'line',
                'smooth': True,
                'data': [5.4, 4.7, 3.8, 4.9, 5.0, 4.2, 4.5, 4.8, 4.7, 4.5, 4.3, 3.6, 4.1, 4.7, 3.9, 4.2, 4.3, 4.5, 3.2, 4.0, 4.1, 3.4, 4.8, 3.9, 4.4, 3.8, 4.2, 4.6, 3.9, 4.3, 4.9],
            },
            {
                'name': 'Позапрошлый месяц',
                'type': 'line',
                'smooth': True,
                'data': [3.6, 3.2, 2.8, 3.1, 1.8, 2.2, 2.6, 2.4, 2.8, 2.7, 3.0, 2.9, 1.8, 2.6, 2.5, 2.8, 2.3, 2.5, 2.9, 1.9, 2.4, 1.5, 2.2, 2.5, 1.2, 1.3, 2.1, 2.3, 1.8, 2.6, 3.3],
            },
        ],
    }

    