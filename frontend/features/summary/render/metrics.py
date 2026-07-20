from nicegui import ui
from core.logger.logger import logger




METRICS = [
    {
        'icon': 'ev_station',
        'key': 'stations',
        'icon_bg': 'bg-blue-600',
        'title': 'ЭЭС в сети',
        'subtitle': 'активных / в работе',
        'value': '246 / 231',
        'delta': '+12',
    },
    {
        'icon': 'currency_ruble',
        'key': 'total_revenue',
        'icon_bg': 'bg-green-600',
        'title': 'Выручка за период',
        'subtitle': 'суммарная',
        'value': '45 812 650 ₽',
        'delta': '+18.7%',
    },
    {
        'icon': 'bolt',
        'key': 'total_energy_kwh',
        'icon_bg': 'bg-yellow-600',
        'title': 'Отпущено электроэнергии',
        'subtitle': 'суммарно',
        'value': '1 263 950 кВт⋅ч',
        'delta': '+15.3%',
    },
    {
        'icon': 'pie_chart',
        'key': 'utilisation',
        'icon_bg': 'bg-purple-600',
        'title': 'Средняя загрузка',
        'subtitle': 'utilisation rate',
        'value': '27.4%',
        'delta': '+3.6 п.п.',
    },
    {
        'icon': 'ev_station',
        'key': 'total_sessions',
        'icon_bg': 'bg-indigo-600',
        'title': 'Зарядных сессий',
        'subtitle': 'всего',
        'value': '18 647',
        'delta': '+16.4%',
    },
    {
        'icon': 'currency_ruble',
        'key': 'avg_revenue_per_station',
        'icon_bg': 'bg-green-600',
        'title': 'Средняя выручка',
        'subtitle': 'на одну ЭЭС',
        'value': '186 233 ₽',
        'delta': '+5.1%',
    },
    {
        'icon': 'person',
        'key': 'avg_revenue_per_session',
        'icon_bg': 'bg-violet-600',
        'title': 'Средняя выручка',
        'subtitle': 'на одну сессию',
        'value': '2 457 ₽',
        'delta': '+1.9%',
    },
    {
        'icon': 'percent',
        'key': 'net_margin_pct',
        'icon_bg': 'bg-orange-600',
        'title': 'Маржинальность сети',
        'subtitle': 'contribution margin',
        'value': '32.8%',
        'delta': '+2.7 п.п.',
    },
    {
        'icon': 'savings',
        'key': 'net_profit',
        'icon_bg': 'bg-lime-600',
        'title': 'Чистая прибыль',
        'subtitle': 'после всех OPEX и налогов',
        'value': '12 745 980 ₽',
        'delta': '+20.3%',
    },
    {
        'icon': 'monitor_heart',
        'key': 'availability',
        'icon_bg': 'bg-cyan-600',
        'title': 'Total доступность',
        'subtitle': 'uptime (взвеш.)',
        'value': '98.36%',
        'delta': '+0.42 п.п.',
    },
]

def calc_delta(current: float, previous: float) -> str:
    if previous in (None, 0):
        return "—"
    delta = (current - previous) / previous * 100
    if delta > 0:
        sign = "+"
    else:
        sign = ''
    return f"{sign}{delta:.1f}%"

def get_metric_value(key:str, data:dict) -> str:
    requested = data['requested_metrics']
    logger.debug(f"requested: {requested}")
    metrics = requested["metrics"]
    margin = requested['margin']

    
    if key == "stations":
        station = requested["station"]
        return f'{station["connected_stations"]} / {station["total_station"]}'
    if key == "total_revenue":
        return f'{metrics["total_revenue"]:,.0f} ₽'.replace(",", " ")
    if key == "total_sessions":
        return f'{metrics["total_sessions"]:,.0f}'.replace(",", " ")
    if key == 'avg_revenue_per_station':
        return f'{metrics["avg_revenue_per_station"]:,.0f}'.replace(",", " ")
    if key == 'total_energy_kwh':
        return f'{metrics["total_energy_kwh"]:,.0f}'.replace(",", " ")
    if key == "utilisation":
        return f'{requested["utilisation"]:.1f}%'
    if key == "net_margin_pct":
        return f'{margin["net_margin_pct"]:.1f}%'
    if key == "avg_revenue_per_session":
        return f'{metrics["avg_revenue_per_session"]:,.0f} ₽'.replace(",", " ")
    if key == 'availability':
        return '-'
    if key == 'net_profit':
        f'{margin["net_profit"]:,.0f} ₽'.replace(",", " ")
    return "-"



def get_metric_delta(key:str, data:dict) -> str:
    requested = data["requested_metrics"]
    comparable = data["comparable_metrics"]

    requested_metrics = requested["margin"]
    comparable_metrics = comparable["margin"]

    if key == "stations":
        return str(
            requested["station"]["connected_stations"]
            - comparable["station"]["connected_stations"]
        )
    if key in (
        "total_revenue",
        "total_sessions",
        "avg_revenue_per_station",
        "avg_revenue_per_session",
        "total_energy_kwh",
        'net_profit'
    ):
        return calc_delta(
            requested_metrics[key],
            comparable_metrics[key]
        )
    if key == 'utilisation':
        return calc_delta(
            requested["utilisation"],
            comparable["utilisation"],
        )
    if key == "net_margin_pct":
        return calc_delta(
            requested["margin"]["net_margin_pct"],
            comparable["margin"]["net_margin_pct"],
        )

    return "—"


def get_delta_class(delta: str) -> str:
    if delta.startswith('-'):
        return "text-red-400"
    if delta == '_':
        return "text-gray-500"
    return "text-green-400"