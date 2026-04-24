from nicegui import ui
from core.formater.formater import formater


def get_metrics(metrics) -> dict:
    m = metrics['metrics']
    total_station = metrics['total_station']

    if total_station == 0:
        income_per_station = 0
    else:
        income_per_station = formater.format_money(
            m['total_revenue'] / total_station
    )
    return {
        "main": [
            {
                'label': 'Доход', 
                'value': formater.format_money(float(m['total_revenue']))
            }
        ],
        "secondary": [
            {
                'label': 'Доход после комиссии', 
                'value': formater.format_money(float(m['my_revenue']))
            },
            {
                'label': 'Комиссия оператора', 
                'value': f"{formater.format_money(float(m['operator_revenue']))} ({m['operator_percent']}%)"
            },
            {
                'label': 'Отгружено энергии (кВт)', 
                'value': formater.format_int(float(m['total_energy_kwh'] or 0))
            },
            {
                'label': 'Доход на станцию', 
                'value': income_per_station
            },
                
               
            ],
            "extra": [
                {
                    'label': 'Кколичество станций:', 
                    'value': formater.format_int(float(total_station)), 
                    'color': 'from-green-50 to-green-100'
                },
                {
                    'label': 'Средний чек:', 
                    'value': formater.format_money(float(m['average_bill'])), 
                    'color': 'from-blue-50 to-blue-100'
                },
                {
                    'label': 'Уникальные пользователи:', 
                    'value': formater.format_int(int(m['total_users'])), 
                    'color': 'from-purple-50 to-purple-100'
                },
                {
                    'label': 'Среднее время (мин):', 
                    'value': formater.format_float(float(m['avg_charge_time'])), 
                    'color': 'from-orange-50 to-orange-100'
                },
                {
                    'label': 'Завершённые сессии:',
                    'value': f"{formater.format_int(int(m['success_sessions']))} / {formater.format_int(int(m['total_sessions']))}",
                    'color': 'from-indigo-50 to-indigo-100'
                },
              
            ]
        }


def metric(title, value, icon=None, color='blue'):
    with ui.card().classes(
        f'flex-1 h-[120px] p-4 rounded-xl \
            shadow-sm border border-gray-200\
            border-l-4 border-{color}-500 \
            flex flex-col justify-between'
    ):
        with ui.row().classes('justify-between items-center'):
            ui.label(title).classes('text-sm\
                                        font-medium\
                                        text-gray-700'
                            )
            if icon:
                ui.icon(icon).classes('text-gray-400')
        ui.label(value).classes('text-3xl font-bold')



def render_total_metric(label, value, size_label, size_value):
    # v = format_money(value)
    with ui.row().classes('items-center gap-4'):
        ui.label(label).classes(f'w-[180px]\
                                 font-semibold\
                                 text-blue-900\
                                 text-{size_label}'
                        )
        ui.label(value).classes(f'font-semibold\
                                text-blue-900\
                                text-{size_value}'
                        )






def render_metrics_list(metrics:list[dict], size_label = 'xl', size_value='xl',  dot = ':'):
    with ui.column().classes('flex-[1.5]'):
        for metric in metrics:
            render_total_metric(
                label=metric['label'] + dot,
                value=metric['value'],
                size_label=size_label,
                size_value=size_value
            )
            if len(metrics) > 1:
                ui.separator().classes('my-3 bg-blue-300 h-[1px]')
            
                               



def get_mock_metrics_main():
    return [
        {'label': 'Оборот', 'value': '1 000 000 ₽'},
    ]


def get_mock_metrics_list():
    return [
        {'label': 'Оборот', 'value': '1 000 000 ₽'},
        {'label': 'Комиссия оператора', 'value': '150 000 ₽'},
        {'label': 'Выручка', 'value': '850 000 ₽'},
        {'label': 'КВт отгружено', 'value': '12 000'},
        {'label': 'Количество сессий', 'value': '320'}
    ]


def get_mock_chart_data():
    return [
        {'value': 400000, 'name': 'ТРЦ РигаМолл'},
        {'value': 250000, 'name': 'ТРЦ "Сиеста" '},
        {'value': 200000, 'name': 'ТК "ЭлитСтрой материалы"'},
        {'value': 150000, 'name': 'ЖК Солнечная Система'},
        {'value': 120000, 'name': 'ЖК Солнечная Система 2'},
        {'value': 80000, 'name': 'Фитнес-клуб "ОХАНА-НЕКРАСОВКА"'},
    ]




def get_mock_stats():
    return [
        {'title': 'Станции', 'value': '6 / 6 онлайн', 'color': 'from-green-50 to-green-100'},
        {'title': 'Средний чек', 'value': '3 100 ₽', 'color': 'from-blue-50 to-blue-100'},
        {'title': 'Пользователи', 'value': '142', 'color': 'from-purple-50 to-purple-100'},
        {'title': 'Среднее время', 'value': '24 мин', 'color': 'from-orange-50 to-orange-100'},
    ]

#  7 | ТЦ 3хГОРКА                     | 3хГорка
#        7 | ТРЦ РигаМолл                   | РигаМолл
#        7 | ТРЦ "Сиеста"                   | ТЦ Сиеста
#        7 | ТК "ЭлитСтрой материалы"       | ЭлитСтрой
#        7 | ЖК Солнечная Система           |
#        7 | ЖК Солнечная Система           |
#        8 | Фитнес-клуб "ОХАНА-НЕКРАСОВКА" | NKR