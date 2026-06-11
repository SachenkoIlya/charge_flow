from nicegui import  ui

from frontend.components.render_top_table import  render_top_table




def render_tables_section(rows: list[dict], reversed_rows:list[dict]):
    with ui.grid(columns=2).classes(
        'w-full gap-4'
    ):
        render_top_table('Топ-5 станций по выручке', 'text-green-400', rows)
        render_top_table('Топ-5 худших станций по выручке', 'text-orange-400', reversed_rows)


TOP_ROWS = [
    {'station': 'ЭЭС-105 ТЦ Мега Химки', 'revenue': '1 245 780', 'load': '38.6%'},
    {'station': 'ЭЭС-042 ТРК Европолис', 'revenue': '1 102 430', 'load': '35.2%'},
    {'station': 'ЭЭС-089 ТЦ Афимолл Сити', 'revenue': '1 087 950', 'load': '34.7%'},
    {'station': 'ЭЭС-077 ТЦ Калейдоскоп', 'revenue': '986 210', 'load': '32.1%'},
    {'station': 'ЭЭС-021 Аэропорт Шереметьево', 'revenue': '872 340', 'load': '29.8%'},
]


REVERS_ROWS = list(reversed(TOP_ROWS))
