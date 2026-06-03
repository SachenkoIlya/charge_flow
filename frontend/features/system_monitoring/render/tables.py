from nicegui import ui

etl_run_columns = [
    ('user_id', 'User', 'w-[80px]'),
    ('type_method', 'Тип', 'w-[180px]'),
    ('run_mode', 'Режим', 'w-[100px]'),
    ('operator', 'Оператор', 'w-[120px]'),
    ('status', 'Статус', 'w-[100px]'),
    ('last_success_at', 'Последний успех', 'w-[220px]'),
    ('created_at', 'Создано', 'w-[220px]'),
    ('run_id', 'Run ID', 'w-[260px]'),
]

def render_table(mode:str, rows: dict, height:int):
       with ui.card().classes(
        f'''
            w-full
            h-[{height}px]
            bg-[#101923]/90
            border border-[#1f2937]
            rounded-xl
            shadow-xl
            p-3
            text-white
            overflow-hidden
        '''
    ):
        ui.label('P&L по станциям').classes('text-base font-bold mb-3')
        with ui.element('div').classes(
            'w-full overflow-x-auto'
        ):
            with ui.element('div').classes(
                'min-w-[1500px]'
            ):
                columns = None
                if mode == 'etl_run':
                    columns = etl_run_columns

                with ui.row().classes(
                    '''
                    min-w-[1400px]
                    text-xs text-gray-400
                    border-b border-[#1f2937]
                    pb-2
                    flex-nowrap
                    '''
                ):
                    for _, label, width in columns:
                        ui.label(label).classes(f'{width} shrink-0 font-semibold')

                for row in rows:
                    with ui.row().classes(
                        '''
                        min-w-[1400px]
                        text-xs
                        border-b border-[#1f2937]
                        py-2
                        flex-nowrap
                        items-center
                        '''
                    ):
                        for key, _, width in columns:
                            value = row.get(key) or '-'
                            if key == 'status':
                                color = 'text-green-400' if value == 'success' else 'text-red-400'
                                ui.label(str(value)).classes(f'{width} shrink-0 font-bold {color}')
                            else:
                                ui.label(str(value)).classes(f'{width} shrink-0 text-gray-200')