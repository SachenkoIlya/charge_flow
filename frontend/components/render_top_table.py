from nicegui import ui

from frontend.features.summary.render.tables_section import render_tables_section


def render_top_table(title: str, title_class: str, rows: list):
    with ui.card().classes(
        '''
        bg-[#101923]/90 border border-[#1f2937]
        rounded-xl shadow-xl p-4 text-white
        '''
    ):
        ui.label(title).classes(f'text-base font-bold mb-4 {title_class}')

        with ui.grid(columns='40px 1fr 100px 90px').classes(
            'w-full text-xs text-gray-400 mb-2'
        ):
            ui.label('#')
            ui.label('Станция')
            ui.label('Выручка, ₽')
            ui.label('Загрузка, %')

        for i, row in enumerate(rows, start=1):
            with ui.grid(columns='40px 1fr 100px 90px').classes(
                'w-full text-sm text-gray-200 py-2 border-t border-[#1f2937]'
            ):
                ui.label(str(i)).classes('text-gray-400')
                ui.label(row['station'])
                ui.label(row['revenue'])
                ui.label(row['load'])


def render_top_tables_dialog(rows, reversed_rows):
    dialog = ui.dialog()

    with dialog:
        with ui.card().classes(
            '''
            w-[1200px] max-w-[95vw]
            bg-[#071019]
            border border-[#1f2937]
            rounded-xl
            p-5
            text-white
            '''
        ):
            with ui.row().classes('w-full items-center justify-between mb-4'):
                ui.label('Рейтинг станций').classes('text-xl font-bold text-white')

                ui.button(
                    icon='close',
                    on_click=dialog.close,
                ).props('flat dense round color=grey')

            render_tables_section(rows, reversed_rows)

    return dialog

# def render_plan_fact_table(title: str, rows: list[dict], height:int):
#     with ui.card().classes(
#         f'''
#             h-[{height}px]
#             bg-[#101923]/90 border border-[#1f2937]
#             rounded-xl shadow-xl p-4 text-white
#         '''
#     ):

#         ui.label(title).classes(
#             'text-base font-bold mb-4 text-white'
#         )
#         with ui.element('div').classes(
#             'h-[195px] overflow-y-auto pr-2'
#         ):
#             with ui.grid(
#                 columns='1.4fr 1fr 1fr 1fr 70px'
#             ).classes(
#                 'w-full text-xs text-gray-400 mb-2'
#             ):

#                 ui.label('Показатель')
#                 ui.label('План')
#                 ui.label('Факт')
#                 ui.label('Отклонение')
#                 ui.label('%')

#             for row in rows:

#                 color = (
#                     'text-green-400'
#                     if row['positive']
#                     else 'text-red-400'
#                 )

#                 with ui.grid(
#                     columns='1.4fr 1fr 1fr 1fr 70px'
#                 ).classes(
#                     '''
#                     w-full
#                     text-sm
#                     text-gray-200
#                     py-2
#                     border-t border-[#1f2937]
#                     items-center
#                     '''
#                 ):

#                     ui.label(row['metric']).classes(
#                         'text-gray-300'
#                     )

#                     ui.label(row['plan'])

#                     ui.label(row['fact'])

#                     ui.label(row['delta']).classes(
#                         color
#                     )

#                     ui.label(row['percent']).classes(
#                         f'{color} font-semibold text-right'
#                     )
def render_plan_fact_table(title: str, rows: list[dict], height:int):

    with ui.card().classes(
        f'''
        h-[{height}px]
        bg-[#101923]/90
        border border-[#1f2937]
        rounded-xl
        shadow-xl
        p-4
        text-white
        '''
    ):

        ui.label(title).classes(
            'text-base font-bold mb-3 shrink-0'
        )

        # HEADER
        with ui.row().classes(
            '''
            w-full
            text-xs text-gray-400
            border-b border-[#1f2937]
            pb-2
            mb-2
            flex-nowrap
            shrink-0
            '''
        ):
            ui.label('Показатель').classes('w-[160px]')
            ui.label('План').classes('w-[120px]')
            ui.label('Факт').classes('w-[120px]')
            ui.label('Отклонение').classes('w-[140px]')
            ui.label('%').classes('w-[60px]')

        # BODY
        with ui.element('div').classes(
            'flex-1 overflow-y-auto pr-1'
        ).style(
            'height: calc(100% - 70px);'
        ):

            for row in rows:
                color = (
                    'text-green-400'
                    if row['positive']
                    else 'text-red-400'
                )
                
                with ui.row().classes(
                    '''
                    w-full
                    text-sm
                    text-gray-200
                    py-3
                    border-b border-[#141c28]
                    flex-nowrap
                    items-center
                    '''
                ):

                    ui.label(row['metric']).classes(
                        'text-gray-300'
                    )

                    ui.label(row['plan'])

                    ui.label(row['fact'])

                    ui.label(row['delta']).classes(
                        color
                    )

                    ui.label(row['percent']).classes(
                        f'{color} font-semibold text-right'
                    )