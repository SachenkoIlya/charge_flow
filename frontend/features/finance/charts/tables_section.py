from nicegui import ui

from frontend.components.metric_card import render_metrics
from frontend.components.pnl_table import render_pnl_table
from frontend.components.render_top_table import render_plan_fact_table


def render_tables_section(rows: list[dict], plan_rows: list[dict]):
    with ui.element('div').classes('grid gap-4 mt-4 w-full').style(
        'grid-template-columns: 2fr 1fr;'
    ):
        render_pnl_table(rows=rows)

        render_plan_fact_table(
            title='План-факт',
            rows=plan_rows,
        )

PNL_ROWS = [
    {
        'station': 'ЭЭС-105 ТЦ Мега Химки',
        'revenue_month': '1 245 780',
        'revenue_total': '12 457 800',
        'energy_cost': '302 450',
        'kwh': '78 540',
        'price_kwh': '3.85',
        'rent_fixed': '100 000',
        'rent_percent': '8%',
        'rent_total': '199 662',
        'operator_own': '74 746',
        'operator_external': '124 578',
        'operator_total': '199 324',
        'operator_percent': '16.0%',
        'ebitda': '422 113',
        'profit': '315 880',
        'margin': '25.4%',
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