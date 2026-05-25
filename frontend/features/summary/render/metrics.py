from frontend.components.metric_card import metric_card
from nicegui import ui



def render_metrics(metrics: list):

    with ui.grid(columns=5).classes(
        'w-full gap-4 mt-6'
    ):

        for metric in metrics:
            metric_card(metric)



METRICS = [
    {
        'icon': 'ev_station',
        'icon_bg': 'bg-blue-600',
        'title': 'ЭЭС в сети',
        'subtitle': 'активных / в работе',
        'value': '246 / 231',
        'delta': '+12',
    },
    {
        'icon': 'currency_ruble',
        'icon_bg': 'bg-green-600',
        'title': 'Выручка за период',
        'subtitle': 'суммарная',
        'value': '45 812 650 ₽',
        'delta': '+18.7%',
    },
    {
        'icon': 'bolt',
        'icon_bg': 'bg-yellow-600',
        'title': 'Отпущено электроэнергии',
        'subtitle': 'суммарно',
        'value': '1 263 950 кВт⋅ч',
        'delta': '+15.3%',
    },
    {
        'icon': 'pie_chart',
        'icon_bg': 'bg-purple-600',
        'title': 'Средняя загрузка',
        'subtitle': 'utilisation rate',
        'value': '27.4%',
        'delta': '+3.6 п.п.',
    },
    {
        'icon': 'monitor_heart',
        'icon_bg': 'bg-cyan-600',
        'title': 'Total доступность',
        'subtitle': 'uptime (взвеш.)',
        'value': '98.36%',
        'delta': '+0.42 п.п.',
    },
    {
        'icon': 'ev_station',
        'icon_bg': 'bg-indigo-600',
        'title': 'Зарядных сессий',
        'subtitle': 'всего',
        'value': '18 647',
        'delta': '+16.4%',
    },
    {
        'icon': 'currency_ruble',
        'icon_bg': 'bg-green-600',
        'title': 'Средняя выручка',
        'subtitle': 'на одну ЭЭС',
        'value': '186 233 ₽',
        'delta': '+5.1%',
    },
    {
        'icon': 'person',
        'icon_bg': 'bg-violet-600',
        'title': 'Средняя выручка',
        'subtitle': 'на одну сессию',
        'value': '2 457 ₽',
        'delta': '+1.9%',
    },
    {
        'icon': 'percent',
        'icon_bg': 'bg-orange-600',
        'title': 'Маржинальность сети',
        'subtitle': 'contribution margin',
        'value': '32.8%',
        'delta': '+2.7 п.п.',
    },
    {
        'icon': 'savings',
        'icon_bg': 'bg-lime-600',
        'title': 'Чистая прибыль',
        'subtitle': 'после всех OPEX и налогов',
        'value': '12 745 980 ₽',
        'delta': '+20.3%',
    },
]