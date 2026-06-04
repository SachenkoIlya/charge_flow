from nicegui import ui
from core.logger.logger import logger
from datetime import datetime

COLUMNS_MAP = {
    'etl_run': [
        'user_id',
        'type_method',
        'run_mode',
        'operator',
        'status',
        'last_success_at',
        'created_at',
        'run_id',
    ],
    'bi_exports': [
        'user_id',
        'type_method',
        'run_mode',
        'operator',
        'status',
        'created_at',
        'updated_at',
        'processed_at',
        'run_id',
    ]
}

def choose_columns(mode:str):
    return COLUMNS_MAP.get(mode, [])


def format_dt(value):
    if not value or value == '-':
        return '-'
    try:
        if isinstance(value, datetime):
            return value.strftime('%d.%m.%Y %H:%M:%S')
        
        dt = datetime.fromisoformat(
            value.replace('Z', '+00:00')
        )
        return dt.strftime('%d.%m.%Y %H:%M:%S')
    except Exception:
        return str(value)
    



def render_table(mode:str, rows: dict, height:int):
    logger.debug(f"[{mode.upper()}]: {rows}")
    CELL_CLASS = 'min-w-[180px] shrink-0'
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
        ui.label(mode.title()).classes('text-base font-bold mb-3')
        with ui.element('div').classes(
            'w-full overflow-x-auto'
        ):
            with ui.element('div').classes(
                'min-w-[1500px]'
            ):
                columns = choose_columns(mode)

                with ui.row().classes(
                    '''
                    min-w-[1400px]
                    text-xs text-gray-400
                    border-b border-[#1f2937]
                    pb-2
                    flex-nowrap
                    '''
                ):
                    for column in columns:
                        ui.label(column).classes(
                            'min-w-[180px] shrink-0 font-semibold'
                        )

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
                        
                        for key in columns:
                            value = row.get(key) or '-'

                            if key in ('created_at', 'last_success_at', 'updated_at', 'processed_at'):
                                value = format_dt(value)

                            if key == 'status':
                                if value == 'success':
                                    color = 'text-green-400'
                                elif value == 'empty':
                                    color = 'text-blue-400'
                                else:
                                    color = 'text-red-400'
                                ui.label(str(value)).classes(f'{CELL_CLASS} font-bold {color}')
                            else:
                                ui.label(str(value)).classes(f'{CELL_CLASS} text-gray-200')