from nicegui import ui
from core.logger.logger import logger

def money(value: float) -> str:
    return f'{value:,.0f} ₽'.replace(',', ' ')

def percent(value: float) -> str:
    return f'{value:.1f}%'


def render_pnl_table(
    rows: list[dict],
    visible_rows: int = 5,
    row_height: int = 52,
):


    columns = [
        ('Станция', 'station_name', 300),
        ('Выручка', 'revenue', 140),
        ('Электроэнергия', 'electricity_cost', 140),
        ('Валовая прибыль', 'gross_profit', 140),
        ('OPEX', 'opex', 140),
        ('EBITDA', 'ebitda', 140),
        ('Налоги', 'taxes', 140),
        ('Чистая прибыль', 'net_profit', 140),
        ('Маржа', 'net_margin', 140),
    ]

    has_vertical_scroll = len(rows) > visible_rows
    body_height = min(len(rows), visible_rows) * row_height

    with ui.card().classes(
        '''
        w-full
        bg-[#101923]/90
        border border-[#1f2937]
        rounded-xl
        shadow-xl
        p-3
        text-white
        overflow-hidden
        '''
    ):
        with ui.element('div').classes(
            'w-full overflow-x-auto'
        ):
            with ui.element('div').classes(
                'min-w-[1500px]'
            ):

                # Заголовок
                with ui.row().classes(
                    '''
                    w-full
                    text-xs
                    text-gray-400
                    border-b
                    border-[#1f2937]
                    pb-3
                    flex-nowrap
                    items-center
                    '''
                ):
                    for label, _, width in columns:
                        ui.label(label).style(
                            f'width: {width}px;'
                        ).classes(
                            'shrink-0 truncate whitespace-nowrap'
                        )

                body_classes = (
                    'w-full overflow-y-auto overflow-x-hidden'
                    if has_vertical_scroll
                    else 'w-full overflow-hidden'
                )

                with ui.element('div').style(
                    f'height: {body_height}px;'
                ).classes(body_classes):

                    for row in rows:
                        with ui.row().style(
                            f'height: {row_height}px;'
                        ).classes(
                            '''
                            w-full
                            text-sm
                            text-gray-200
                            border-b
                            border-[#141c28]
                            flex-nowrap
                            items-center
                            hover:bg-[#16212d]
                            transition-colors
                            '''
                        ):
                            for _, key, width in columns:
                                value = row.get(key, '—')

                                cls = (
                                    'shrink-0 truncate whitespace-nowrap'
                                )

                                if key == 'station_name':
                                    cls += ' font-medium text-white'

                                elif key in {
                                    'electricity_cost',
                                    'opex',
                                    'taxes',
                                }:
                                    cls += ' text-orange-300'

                                elif key in {
                                    'gross_profit',
                                    'ebitda',
                                }:
                                    cls += ' font-semibold'

                                elif key in {
                                    'net_profit',
                                    'net_margin',
                                }:
                                    cls += ' text-green-400 font-semibold'

                                if key not in {'station_name', 'net_margin'}:
                                    cell = ui.label(money(value)).style(
                                        f'width: {width}px;'
                                    ).classes(cls)
                                    
                                if key == 'net_margin':
                                    cell = ui.label(percent(value)).style(
                                        f'width: {width}px;'
                                    ).classes(cls)

                                if key == 'station_name':
                                    cell.tooltip(str(value))