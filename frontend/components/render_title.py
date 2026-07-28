from nicegui import ui

from frontend.components.calendar import get_calendar
from core.logger.logger import logger
from nicegui import app
import asyncio 

FILTER_MAP = {
    'summary': {
       'toggle': [
            {'label': '6 МЕС', 'value': '6m'},
            {'label': '1 ГОД', 'value': '1y'},
            {'label': 'ВСЕ', 'value': 'all'},
        ],
            'default_value': 'all',
    },
    'finance': {
        'toggle': [
            {'label': '6 МЕС', 'value': '6m'},
            {'label': '1 ГОД', 'value': '1y'},
            {'label': 'ВСЕ', 'value': 'all'},
        ],
        'default_value': 'all',
    },
    'investments_and_expenses': {
        'toggle': [
            {'label': 'CAPEX', 'value': 'capex'},
            {'label': 'OPEX', 'value': 'opex'},
        ],
        'default_value': 'capex',
    },
    'system': {
        'toggle': [
            {'label': 'etl_run', 'value': 'etl_run'},
            {'label': 'bi_exports', 'value': 'bi_exports'},
        ],
        'default_value': 'etl_run',
    }
}
def get_selected_label(e):
    raw_value = e.args
    if isinstance(raw_value, list) and len(raw_value) > 1:
        payload = raw_value[1]
    if isinstance(payload, dict):
        return payload.get('label')    
    if isinstance(raw_value, str):
        return raw_value
    return None

def resolve_toggle_value(data: dict, event_value: str) -> str | None:
    toggle_options = {
        item['label']: item['value']
        for item in data['toggle']
    }
    return toggle_options.get(event_value)


def get_data_from_map(page_key: str):
    data = FILTER_MAP.get(page_key, None)
    if not data: 
        return None
    return data


async def render_title(
    label,
    label_aggre,
    stations,
    page_key,
    on_date_change=None,
):
    pages = app.storage.user.get('pages', {})
    page_state = pages.setdefault(page_key, {})

    # -----------------------------
    # 1. Значения по умолчанию
    # -----------------------------
    page_state.setdefault('station_ids', [])
    page_state.setdefault('toggle_value', 'all')

    selected_station_ids = page_state['station_ids']

    # -----------------------------
    # 2. Функция отображения станций
    # -----------------------------
    def station_display_value(value):
        if not value:
            return 'Все станции'

        if len(value) == 1:
            station_id = value[0]
            return stations.get(station_id, '1 станция')
        count = len(value)

        if 11 <= count % 100 <= 14:
            word = 'станций'
        elif count % 10 == 1:
            word = 'станция'
        elif 2 <= count % 10 <= 4:
            word = 'станции'
        else:
            word = 'станций'

        return f'Выбрано: {count} {word}'

    # -----------------------------
    # 3. Обработчик выбора станции
    # -----------------------------
    async def handle_station_change(e):
        station_ids = e.value or []

        page_state['station_ids'] = station_ids
        app.storage.user['pages'] = pages

        if on_date_change:
            asyncio.create_task(on_date_change())

    # -----------------------------
    # 4. Обработчик периода
    # -----------------------------
    async def handle_toggle(e):
        page_state['toggle_value'] = e.value
        app.storage.user['pages'] = pages

        if on_date_change:
            asyncio.create_task(on_date_change())

    # -----------------------------
    # 5. UI
    # -----------------------------
    with ui.row().classes(
        'w-full items-center justify-between'
    ):

        # Заголовок
        with ui.column().classes('gap-0'):
            ui.label(label).classes(
                'text-2xl font-bold text-white'
            )
            ui.label(label_aggre).classes(
                'text-sm text-slate-400'
            )

        # Фильтры
        with ui.row().classes(
            '''
            items-center
            gap-4
            px-3 py-2
            rounded-2xl
            bg-[#0f1822]
            border border-[#243244]
            '''
        ):

            period_toggle = ui.toggle(
                {
                    '6m': '6 МЕС',
                    '1y': '1 ГОД',
                    'all': 'ВСЕ',
                },
                value=page_state['toggle_value'],
            ).props(
                'no-caps unelevated'
            )

            period_toggle.on(
                'update:model-value',
                handle_toggle,
            )

            # -----------------------------
            # SELECT СТАНЦИЙ
            # -----------------------------
            selected_station_ids = page_state.get('station_ids', [])

            display_value = station_display_value(selected_station_ids)

            station_select = ui.select(
                options=stations,
                value=selected_station_ids,
                multiple=True,
                on_change=handle_station_change,
            ).props(
                f'''
                outlined
                dense
                options-dense
                clearable
                dropdown-icon=expand_more
                display-value="{display_value}"
                '''
            ).classes(
                'w-[285px]'
            )


            
# async def render_title(
    # label: str,
    # label_aggre: str,
    # page_key: str,
    # stations: dict[int, str] | None = None,
    # on_date_change=None,
# ):
    # pages = app.storage.user.setdefault('pages', {})
    # page_state = pages.setdefault(page_key, {})
# 
    # page_state.setdefault('station_ids', [])
# 
    # async def handle_station_change(e):
        # station_id = e.value
# 
        # page_state['station_ids'] = (
            # [station_id]
            # if station_id is not None
            # else []
        # )
# 
        # app.storage.user['pages'] = pages
# 
        # if on_date_change:
            # asyncio.create_task(on_date_change())
# 
    # with ui.row().classes(
        # '''
        # w-full
        # items-start
        # justify-between
        # mb-0
        # '''
    # ):
        # with ui.column().classes('gap-0'):
            # ui.label(label).classes(
                # '''
                # text-3xl
                # font-bold
                # text-white
                # leading-tight
                # '''
            # )
# 
            # if page_key == 'summary':
                # ui.label(label_aggre).classes(
                    # 'text-sm text-gray-400 mt-1'
                # ).style(
                    # 'white-space: pre-line'
                # )
# 
        # Общий контейнер фильтров
        # with ui.row().classes(
            # '''
            # items-center
            # gap-8
            # px-3
            # py-2
            # rounded-2xl
            # bg-[#0f1822]
            # border
            # border-[#243244]
            # '''
        # ):
            # data = get_data_from_map(page_key)
# 
            # if data:
                # toggle_items = data.get('toggle', [])
# 
                # options = {
                    # item['label']: item['value']
                    # for item in toggle_items
                # }
# 
                # allowed_values = set(options.values())
                # current_value = page_state.get('toggle_value')
# 
                # if current_value not in allowed_values:
                    # current_value = data.get('default_value')
                    # page_state['toggle_value'] = current_value
# 
                # value_to_label = {
                    # item['value']: item['label']
                    # for item in toggle_items
                # }
# 
                # current_label = value_to_label.get(current_value)
# 
                # period_toggle = ui.toggle(
                    # list(options.keys()),
                    # value=current_label,
                # ).props(
                    # 'unelevated toggle-color=green'
                # ).classes(
                    # '''
                    # bg-[#101923]
                    # border
                    # border-[#1f2937]
                    # rounded-xl
                    # p-1
                    # text-sm
                    # font-bold
                    # '''
                # )
# 
                # async def handle_toggle(e):
                    # selected_label = get_selected_label(e)
# 
                    # new_value = resolve_toggle_value(
                        # data,
                        # selected_label,
                    # )
# 
                    # if new_value is None:
                        # return
# 
                    # if page_state.get('toggle_value') == new_value:
                        # return
# 
                    # page_state['toggle_value'] = new_value
                    # app.storage.user['pages'] = pages
# 
                    # if on_date_change:
                        # asyncio.create_task(on_date_change())
# 
                # period_toggle.on(
                    # 'update:model-value',
                    # handle_toggle,
                # )
# 
            # selected_station_ids = page_state.get(
                # 'station_ids',
                # [],
            # )
# 
            # selected_station_id = (
                # selected_station_ids[0]
                # if selected_station_ids
                # else None
            # )
# 
            # logger.warning(selected_station_ids)
# 
            # if stations:
                # ui.select(
                    # options=stations,
                    # value=selected_station_id,
                    # label='Станция',
                    # on_change=handle_station_change,
                # ).props(
                    # '''
                    # outlined
                    # dense
                    # options-dense
                    # clearable
                    # '''
                # ).classes(
                    # 'w-72'
                # )