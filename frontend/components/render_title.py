from nicegui import ui

from frontend.components.calendar import get_calendar
from core.logger.logger import logger
from nicegui import app


MAP = {
    'finance': {
        'toggle': ['6 МЕС', '1 ГОД', 'ВСЕ'],
        'default_value': 'ВСЕ',
    },
      'investments_and_expenses': {
        'toggle': ['CAPEX', 'OPEX'],
        'default_value': 'CAPEX',
    
    },
    'system': {
        'toggle': ['etl_run', 'bi_exports'],
        'default_value': 'etl_run',
    
    }
}


def get_data_from_map(page_key: str):
    data = MAP.get(page_key, None)
    if not data: 
        return None
    return data

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
            if page_key in {'summary'}:
                ui.label(label_aggre).classes(
                    'text-sm text-gray-400 mt-1'
                ).style(
                    'white-space: pre-line'
                )
               
        data = get_data_from_map(page_key)

        if data:
            page = app.storage.user.get('pages', {})
            page_state = page.setdefault(page_key, {})
            
            toggle = data.get('toggle')
            current_value = page_state.get('toggle_value')

            if current_value not in toggle:
                current_value = data.get('default_value')
                page_state['toggle_value'] = current_value
            
            
            period_toggle = ui.toggle(
                toggle,
                value=current_value,
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
            async def handle_toggle(e):
                page = app.storage.user.setdefault('pages', {})
                page_state = page.setdefault(page_key, {})

                old_value = page_state.get('toggle_value')
                raw_value = e.args
                if isinstance(raw_value, list) and len(raw_value) > 1:
                    new_value = e.args[1].get('label')
                else:
                    new_value = raw_value

                if old_value == new_value:
                    return

                page_state['toggle_value'] = new_value
                app.storage.user['pages'] = page

                if on_date_change:
                    await on_date_change()

            period_toggle.on(
                'update:model-value',
                handle_toggle
            )
           
        else:
            await get_calendar(
                page_key=page_key,
                on_change_date=on_date_change,
            )
    