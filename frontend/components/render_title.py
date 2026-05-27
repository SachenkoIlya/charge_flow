from nicegui import ui

from frontend.components.calendar import get_calendar
from core.logger.logger import logger

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
            period_toggle = ui.toggle(
                ['6 МЕС', '1 ГОД', 'ВСЕ'],
                value='ВСЕ',
            ).props(
                'unelevated toggle-color=green'
            ).classes(
                '''
                bg-[#101923]
                border border-[#1f2937]
                rounded-2xl
                p-1
                text-sm
                font-bold
                '''
            )
            period_toggle.on(
                'update:model-value',
                lambda e: logger.debug(f"period:, {e.args}")
            )
          
        else:
            await get_calendar(
                page_key=page_key,
                on_change_date=on_date_change,
            )
    