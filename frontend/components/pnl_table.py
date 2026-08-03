from nicegui import ui

# def render_pnl_table(rows: list[dict], height:int=600):
#         # h-[{height}px]
#        with ui.card().classes(
#         f'''
#             w-full
#             bg-[#101923]/90
#             border border-[#1f2937]
#             rounded-xl
#             shadow-xl
#             p-3
#             text-white
#             overflow-hidden
#         '''
#     ):
#         # ui.label('P&L по станциям').classes('text-base font-bold mb-3')
#         with ui.element('div').classes(
#             'w-full overflow-x-auto'
#         ):
#             with ui.element('div').classes(
#                 'min-w-[1500px]'
#             ):
#                 columns = [
#                     ('Станция', 'station', 300),
#                     ('Выручка', 'revenue', 150),
#                     ('Электроэнергия', 'energy_cost', 160),
#                     ('Валовая прибыль', 'gross_profit', 170),
#                     ('OPEX', 'opex', 140),
#                     ('EBITDA', 'ebitda', 140),
#                     ('Налоги', 'taxes', 130),
#                     ('Чистая прибыль', 'net_profit', 170),
#                     ('Маржа', 'margin', 110),
#                 ]
#                 with ui.row().classes(
#                     '''
#                     min-w-[1400px]
#                     text-xs text-gray-400
#                     border-b border-[#1f2937]
#                     pb-2
#                     flex-nowrap
#                     '''
#                 ):
#                     for label, _, width in columns:
#                         ui.label(label).style(
#                             f'width: {width}px'
#                         ).classes(
#                             'shrink-0 truncate whitespace-nowrap'
#                         )

#                 for row in rows:
#                     with ui.row().classes(
#                         '''
#                         w-full
#                         text-sm 
#                         text-gray-200
#                         py-4
#                         border-b
#                         border-[#141c28]
#                         flex-nowrap
#                         '''
#                     ):
#                         for _, key, width in columns:

#                             cls = 'shrink-0 truncate whitespace-nowrap'

#                             if key == 'margin':
#                                 cls += ' text-green-400 font-semibold'

#                             ui.label(row[key]).style(
#                                 f'width: {width}px'
#                             ).classes(cls)


def render_pnl_table(
    rows: list[dict],
    visible_rows: int = 5,
    row_height: int = 52,
):
    columns = [
        ('Станция', 'station', 300),
        ('Выручка', 'revenue', 130),
        ('Электроэнергия', 'energy_cost', 130),
        ('Валовая прибыль', 'gross_profit', 130),
        ('OPEX', 'opex', 130),
        ('EBITDA', 'ebitda', 130),
        ('Налоги', 'taxes', 130),
        ('Чистая прибыль', 'net_profit', 130),
        ('Маржа', 'margin', 110),
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

                                if key == 'station':
                                    cls += ' font-medium text-white'

                                elif key in {
                                    'energy_cost',
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
                                    'margin',
                                }:
                                    cls += ' text-green-400 font-semibold'

                                cell = ui.label(str(value)).style(
                                    f'width: {width}px;'
                                ).classes(cls)

                                if key == 'station':
                                    cell.tooltip(str(value))