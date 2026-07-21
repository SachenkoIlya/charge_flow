
#   'icon': 'ev_station',
#         'key': 'stations',
#         'icon_bg': 'bg-blue-600',
#         'title': 'ЭЭС в сети',
#         'subtitle': 'активных / в работе',
#         'value': '246 / 231',
#         'delta': '+12',

#    'icon': 'ev_station',
#         'key': 'stations',
#         'icon_bg': 'bg-blue-600',
#         'title': 'ЭЭС в сети',
#         'subtitle': 'активных / в работе',
#         'value': '246 / 231',
#         'delta': '+12',

FINANCE_METRICS = [
    {
        'icon': 'payments',
        'icon_bg': 'bg-green-500',
        'key': 'total_revenue',
        'title': 'Выручка сети (мес.)',
        'subtitle': 'общий оборот',
        'value': '45 812 650 ₽',
        'delta': '+18.7%',
    },

    {
        'icon': 'trending_up',
        'icon_bg': 'bg-orange-500',
        'title': 'EBITDA сети',
        'key': 'ebitda',
        'subtitle': 'опер. прибыль',
        'value': '15 246 320 ₽',
        'delta': '+2.4 п.п.',
    },

    {
        'icon': 'show_chart',
        'icon_bg': 'bg-purple-500',
        'title': 'Чистая прибыль сети',
        'key': 'net_profit',
        'subtitle': 'после налогов',
        'value': '12 745 980 ₽',
        'delta': '+3.1 п.п.',
    },

    {
        'icon': 'account_balance_wallet',
        'icon_bg': 'bg-blue-500',
        'title': 'CAPEX (всего)',
        'key': 'capex',
        'subtitle': 'инвестиции в сеть',
        'value': '152 450 000 ₽',
        'delta': '657 978 ₽ / ЭЗС',
        'value_class': 'text-lg',
    },

    {
        'icon': 'savings',
        'icon_bg': 'bg-cyan-500',
        'title': 'Накопленный cash flow',
        'subtitle': 'денежный поток',
        'key': 'cash_flow',
        'value': '28 950 760 ₽',
        'delta': '+5 780 450 ₽',
        'value_class': 'text-lg',
    },

    {
        'icon': 'inventory_2',
        'icon_bg': 'bg-yellow-500',
        'title': 'Средняя окупаемость',
        'key': 'payback_period',
        'subtitle': 'прогноз ROI',
        'value': '18.6 мес.',
        'delta': 'прогноз: 16.2 мес.',
    },
]

def get_metrics_value(key:str, data:dict)->str:
    metrics = data["metrics"]
    capex = data['investment']['capex']
    total_capex = str(
        sum(
            capex[m] for m in capex
        )
    )
    k = {
        'total_revenue':  f"{metrics['total_revenue']:,.0f} ₽".replace(",", " "),
        'ebitda': f"{metrics['ebitda']:,.0f} ₽".replace(",", " "),
        'net_profit': f"{metrics['net_profit']:,.0f} ₽".replace(",", " "),
        'capex': f"{total_capex :,.0f} ₽".replace(",", " "),
        'cash_flow': f"{metrics['cash_flow']:,.0f} ₽".replace(",", " "),
        'payback_period': '-'
    }
    return k.get(key, '-')


def get_metric_delta(key:str, data:dict)->str:
    return '-'
