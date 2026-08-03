from nicegui import ui

from frontend.components.metric_card import render_metrics
from frontend.components.pnl_table import render_pnl_table
from frontend.components.render_top_table import render_plan_fact_table


def render_tables_section(rows: list[dict], plan_rows: list[dict], height:int=470):
    
    with ui.element('div').classes('grid gap-4 mt-4 w-full').style(
        'grid-template-columns: 2.02fr 1fr;'
    ):
        render_pnl_table(rows=rows, height=height)


PNL_ROWS = [
    {
        'station': 'ЭЗС-106 Рига Молл',
        'revenue': '12 457 800',
        'energy_cost': '302 450',
        'gross_profit': '12 155 350',
        'opex': '11 733 237',
        'ebitda': '422 113',
        'taxes': '106 233',
        'net_profit': '315 880',
        'margin': '2.5%',
    },
    {
        'station': 'ЭЗС-042 ТРК Европолис',
        'revenue': '1 102 430',
        'energy_cost': '268 990',
        'gross_profit': '833 440',
        'opex': '469 382',
        'ebitda': '364 058',
        'taxes': '96 677',
        'net_profit': '267 381',
        'margin': '24.3%',
    },
    {
        'station': 'ЭЗС-089 ТЦ Афимолл Сити',
        'revenue': '1 087 950',
        'energy_cost': '265 230',
        'gross_profit': '822 720',
        'opex': '463 973',
        'ebitda': '358 747',
        'taxes': '107 874',
        'net_profit': '250 873',
        'margin': '23.1%',
    },
    {
        'station': 'ЭЗС-077 ТЦ Капитолий',
        'revenue': '986 210',
        'energy_cost': '240 110',
        'gross_profit': '746 100',
        'opex': '415 310',
        'ebitda': '330 790',
        'taxes': '104 360',
        'net_profit': '226 430',
        'margin': '22.9%',
    },
    {
        'station': 'ЭЗС-021 Аэропорт Шереметьево',
        'revenue': '872 340',
        'energy_cost': '212 890',
        'gross_profit': '659 450',
        'opex': '363 230',
        'ebitda': '296 220',
        'taxes': '97 477',
        'net_profit': '198 743',
        'margin': '22.8%',
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