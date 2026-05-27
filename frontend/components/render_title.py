from nicegui import ui

from frontend.components.calendar import get_calendar


async def render_title(
    label: str, 
    label_aggre: str,
    page_key: str,
    on_date_change=None,

):
    with ui.row().classes('w-full items-start justify-between mb-6'):

        with ui.column().classes('gap-0'):
            ui.label(label).classes(
                'text-3xl font-bold text-white leading-tight'
            )

            ui.label(label_aggre).classes(
                'text-sm text-gray-400 mt-1'
            )
        if page_key in {'finance'}:
            ui.toggle(
                ['6 мес', '1 год', 'Все'],
                value='6 мес'
            )
        else:
            await get_calendar(
                page_key=page_key,
                on_change_date=on_date_change,
            )
    