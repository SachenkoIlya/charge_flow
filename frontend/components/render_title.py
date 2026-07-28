from nicegui import ui, app 

from frontend.components.calendar import get_calendar
from core.logger.logger import logger
import asyncio 


ui.add_css("""
.station-multi-select .q-field__native > span {
    display: none;
}

.station-multi-select .q-field__native {
    color: transparent;
}
""", shared=True)


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
    label: str,
    label_aggre: str,
    page_key: str,
    stations: dict=None,
    on_date_change=None,
):
    # -----------------------------------
    # 1. Конфигурация экрана
    # -----------------------------------
    filter_config = FILTER_MAP.get(page_key, {})

    toggle_items = filter_config.get('toggle', [])
    default_toggle_value = filter_config.get('default_value')

    # Пока станции нужны только этим экранам
    show_stations = page_key in {
        'summary',
        'finance',
    }

    toggle_options = {
        item['value']: item['label']
        for item in toggle_items
    }

    # -----------------------------------
    # 2. State страницы
    # -----------------------------------
    pages = app.storage.user.get('pages', {})
    page_state = pages.setdefault(page_key, {})

    page_state.setdefault(
        'toggle_value',
        default_toggle_value,
    )

    if show_stations:
        page_state.setdefault(
            'station_ids',
            [],
        )

    app.storage.user['pages'] = pages

    selected_station_ids = (
        page_state.get('station_ids', [])
        if show_stations
        else []
    )

    # -----------------------------------
    # 3. Отображение выбранных станций
    # -----------------------------------
    def station_display_value(value):
        if not value:
            return 'Все станции'

        # Если пользователь руками выбрал все станции
        if stations and len(value) == len(stations):
            return 'Все станции'

        if len(value) == 1:
            station_id = value[0]

            return stations.get(
                station_id,
                '1 станция',
            )

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

    # -----------------------------------
    # UI элементы, которые обновляются
    # из handlers
    # -----------------------------------
    station_label = None

    # -----------------------------------
    # 4. Handler станций
    # -----------------------------------
    async def handle_station_change(e):
        station_ids = e.value or []

        page_state['station_ids'] = station_ids
        app.storage.user['pages'] = pages

        if station_label:
            station_label.set_text(
                station_display_value(station_ids)
            )

        if on_date_change:
            asyncio.create_task(
                on_date_change()
            )
    # -----------------------------------
    # 5. Handler toggle
    # -----------------------------------
    async def handle_toggle(e):
        selected_label = get_selected_label(e)
        new_value = resolve_toggle_value(
            filter_config,
            selected_label,
        )
        if new_value is None:
            return
        if page_state.get('toggle_value') == new_value:
            return
        page_state['toggle_value'] = new_value
        app.storage.user['pages'] = pages
        if on_date_change:
            asyncio.create_task(on_date_change())
    # -----------------------------------
    # 6. HEADER
    # -----------------------------------
    with ui.row().classes(
        '''
        w-full
        items-center
        justify-between
        '''
    ):

        # -------------------------------
        # Левая часть
        # -------------------------------
        with ui.column().classes(
            'gap-0'
        ):
            ui.label(
                label
            ).classes(
                '''
                text-2xl
                font-bold
                text-white
                '''
            )

            ui.label(
                label_aggre
            ).classes(
                '''
                text-sm
                text-slate-400
                '''
            )

        # -------------------------------
        # Правая часть — фильтры
        # -------------------------------
        if toggle_options or (
            show_stations and stations
        ):

            with ui.row().classes(
                '''
                items-center
                gap-4
                px-3
                py-2
                rounded-2xl
                bg-[#0f1822]
                border
                border-[#243244]
                '''
            ):

                # -----------------------
                # TOGGLE
                # -----------------------
                if toggle_options:

                    period_toggle = ui.toggle(
                        toggle_options,
                        value=page_state[
                            'toggle_value'
                        ],
                    ).props(
                        '''
                        no-caps
                        unelevated
                        '''
                    )

                    period_toggle.on(
                        'update:model-value',
                        handle_toggle,
                    )

                # -----------------------
                # STATION SELECT
                # -----------------------
                if show_stations and stations:

                    with ui.element(
                        'div'
                    ).classes(
                        '''
                        relative
                        w-[285px]
                        '''
                    ):

                        station_select = ui.select(
                            options=stations,
                            value=selected_station_ids,
                            multiple=True,
                            on_change=(
                                handle_station_change
                            ),
                        ).props(
                            '''
                            outlined
                            dense
                            options-dense
                            clearable
                            dropdown-icon=expand_more
                            '''
                        ).classes(
                            '''
                            w-full
                            station-multi-select
                            '''
                        )

                        station_label = ui.label(
                            station_display_value(
                                selected_station_ids
                            )
                        ).classes(
                            '''
                            absolute
                            left-3
                            top-1/2
                            -translate-y-1/2
                            text-sm
                            text-white
                            pointer-events-none
                            max-w-[210px]
                            truncate
                            '''
                        )
# async def render_title(
#     label,
#     label_aggre,
#     page_key,
#     stations=None,
#     on_date_change=None,
# ):
#     pages = app.storage.user.get('pages', {})
#     page_state = pages.setdefault(page_key, {})

#     page_state.setdefault('station_ids', [])
#     page_state.setdefault('toggle_value')

#     selected_station_ids = page_state['station_ids']

#     def station_display_value(value):
#         if not value:
#             return 'Все станции'

#         if len(value) == len(stations):
#             return 'Все станции'

#         if len(value) == 1:
#             station_id = value[0]
#             return stations.get(station_id, '1 станция')

#         count = len(value)

#         if 11 <= count % 100 <= 14:
#             word = 'станций'
#         elif count % 10 == 1:
#             word = 'станция'
#         elif 2 <= count % 10 <= 4:
#             word = 'станции'
#         else:
#             word = 'станций'

#         return f'Выбрано: {count} {word}'

#     # сюда позже положим label
#     station_label = None

#     async def handle_station_change(e):
#         station_ids = e.value or []

#         page_state['station_ids'] = station_ids
#         app.storage.user['pages'] = pages

#         if station_label:
#             station_label.set_text(
#                 station_display_value(station_ids)
#             )

#         # пока занимаемся фронтом, можно временно отключить
#         if on_date_change:
#             asyncio.create_task(on_date_change())

#     async def handle_toggle(e):
#         page_state['toggle_value'] = e.value
#         app.storage.user['pages'] = pages

#         if on_date_change:
#             asyncio.create_task(on_date_change())


#     filter_config = FILTER_MAP.get(page_key, {})
#     toggle_items = filter_config.get('toggle', [])
#     default_toggle_value = filter_config.get('default_value')

#     toggle_options = {
#         item['value']: item['label']
#         for item in toggle_items
#     }
#     with ui.row().classes(
#         'w-full items-center justify-between'
#     ):

#         with ui.column().classes('gap-0'):
#             ui.label(label).classes(
#                 'text-2xl font-bold text-white'
#             )

#             ui.label(label_aggre).classes(
#                 'text-sm text-slate-400'
#             )
        
#         with ui.row().classes(
#             '''
#             items-center
#             gap-4
#             px-3 py-2
#             rounded-2xl
#             bg-[#0f1822]
#             border border-[#243244]
#             '''
#         ):

#             if toggle_options:
#                 period_toggle = ui.toggle(
#                     toggle_options,
#                     value=page_state['toggle_value'],
#                 ).props(
#                     'no-caps unelevated'
#                 )

#                 period_toggle.on(
#                     'update:model-value',
#                     handle_toggle,
#                 )

#             # -----------------------------
#             # SELECT СТАНЦИЙ
#             # -----------------------------
#             with ui.element('div').classes(
#                 'relative w-[285px]'
#             ):

#                 station_select = ui.select(
#                     options=stations,
#                     value=selected_station_ids,
#                     multiple=True,
#                     on_change=handle_station_change,
#                 ).props(
#                     '''
#                     outlined
#                     dense
#                     options-dense
#                     clearable
#                     dropdown-icon=expand_more
#                     '''
#                 ).classes(
#                     'w-full station-multi-select'
#                 )

#                 station_label = ui.label(
#                     station_display_value(
#                         selected_station_ids
#                     )
#                 ).classes(
#                     '''
#                     absolute
#                     left-3
#                     top-1/2
#                     -translate-y-1/2
#                     text-sm
#                     text-white
#                     pointer-events-none
#                     max-w-[210px]
#                     truncate
#                     '''
#                 )

            
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