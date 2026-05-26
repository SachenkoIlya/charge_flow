from nicegui import  ui

from frontend.components.render_top_table import  render_top_table




def render_tables_section(rows: list[dict], reversed_rows:list[dict]):
    with ui.grid(columns=2).classes('w-full gap-4 mt-4'):
        render_top_table('Топ-5 станций по выручке', 'text-green-400', rows)
        render_top_table('Топ-5 худших станций по выручке', 'text-orange-400', reversed_rows)