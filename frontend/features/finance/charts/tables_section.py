from nicegui import ui

from frontend.components.render_top_table import render_plan_fact_table


def render_tables_section(rows: list[dict], plan_rows: list[dict]):
    with ui.element('div').classes('grid gap-4 mt-4 w-full').style(
        'grid-template-columns: 2fr 1fr;'
    ):
        render_plan_fact_table(
            title='P&L по станциям',
            rows=rows,
        )

        render_plan_fact_table(
            title='План-факт',
            rows=plan_rows,
        )


METRICS_PNL = [
    {
        'title': 'Выручка сети',
        'subtitle': 'месячный оборот',
        'value': '45 812 650 ₽',
        'delta': '+18.7%',
        'icon': 'payments',
        'icon_bg': 'bg-[#22c55e]',
    },
    {
        'title': 'EBITDA сети',
        'subtitle': 'операц. прибыль',
        'value': '15 246 320 ₽',
        'delta': '+2.4 п.п.',
        'icon': 'trending_up',
        'icon_bg': 'bg-[#f97316]',
    },
    {
        'title': 'Чистая прибыль сети',
        'subtitle': 'после налогов',
        'value': '12 745 980 ₽',
        'delta': '+3.1 п.п.',
        'icon': 'show_chart',
        'icon_bg': 'bg-[#a855f7]',
    },
    {
        'title': 'CAPEX (всего)',
        'subtitle': 'инвестиции в сеть',
        'value': '152 450 000 ₽',
        'delta': '657 978 ₽ / ЭЗС',
        'icon': 'account_balance_wallet',
        'icon_bg': 'bg-[#3b82f6]',
        'value_class': 'text-lg',
    },
    {
        'title': 'Накопленный cash flow',
        'subtitle': 'денежный поток',
        'value': '28 950 760 ₽',
        'delta': '+5 780 450 ₽',
        'icon': 'savings',
        'icon_bg': 'bg-[#06b6d4]',
        'value_class': 'text-lg',
    },
    {
        'title': 'Средняя окупаемость',
        'subtitle': 'прогноз ROI',
        'value': '18.6 мес.',
        'delta': 'прогноз: 16.2 мес.',
        'icon': 'receipt_long',
        'icon_bg': 'bg-[#eab308]',
    },
]


PLAN_FACT_ROWS = [
    {
        'metric': 'Выручка',
        'plan': '44 000 000 ₽',
        'fact': '45 812 650 ₽',
        'delta': '+1 812 650 ₽',
        'percent': '+4.1%',
        'positive': True,
    },
    {
        'metric': 'EBITDA',
        'plan': '13 200 000 ₽',
        'fact': '15 246 320 ₽',
        'delta': '+2 046 320 ₽',
        'percent': '+15.5%',
        'positive': True,
    },
    {
        'metric': 'Чистая прибыль',
        'plan': '10 800 000 ₽',
        'fact': '12 745 980 ₽',
        'delta': '+1 945 980 ₽',
        'percent': '+18.0%',
        'positive': True,
    },
    {
        'metric': 'Затраты на эл/энергию',
        'plan': '11 500 000 ₽',
        'fact': '10 254 890 ₽',
        'delta': '-1 245 110 ₽',
        'percent': '-10.8%',
        'positive': False,
    },
    {
        'metric': 'Аренда',
        'plan': '4 200 000 ₽',
        'fact': '4 086 420 ₽',
        'delta': '-113 580 ₽',
        'percent': '-2.7%',
        'positive': False,
    },
    {
        'metric': 'Комиссия оператора',
        'plan': '2 800 000 ₽',
        'fact': '2 565 130 ₽',
        'delta': '-234 870 ₽',
        'percent': '-8.4%',
        'positive': False,
    },
    {
        'metric': 'OPEX (прочее)',
        'plan': '2 100 000 ₽',
        'fact': '1 987 450 ₽',
        'delta': '-112 550 ₽',
        'percent': '-5.4%',
        'positive': False,
    },
    {
        'metric': 'Налоги',
        'plan': '2 100 000 ₽',
        'fact': '1 927 780 ₽',
        'delta': '-172 220 ₽',
        'percent': '-8.2%',
        'positive': False,
    },
]