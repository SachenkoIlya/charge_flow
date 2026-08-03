from nicegui import ui


# def render_opex_details(
#     data: dict,
#     visible_rows:int=3,
#     row_height: int = 52,

# ) -> None:
   
#     labels = {
#         'electricity_compensation': 'Электроэнергия',
#         'rent_payment': 'Аренда',
#         'operator_commission': 'Комиссия оператора',
#         'service_maintenance': 'Сервисное обслуживание',
#         'internet_and_connection': 'Интернет и связь',
#         'insurance': 'Страхование',
#         'other_expenses': 'Прочие расходы',
#     }
    
#     rows = [
#         {
#             'key': key,
#             'label': label,
#             'value': float(data.get(key, 0) or 0),
#         }
#         for key, label in labels.items()
#     ]

#     has_vertical_scroll = len(rows) > visible_rows
#     body_height = min(len(rows), visible_rows) * row_height

#     total = sum(row['value'] for row in rows)

#     with ui.card().classes(
#         '''
#         w-full
#         h-full
#         bg-[#101923]/90
#         border border-[#1f2937]
#         rounded-xl
#         shadow-xl
#         p-4
#         text-white
#         '''
#     ):
#         ui.label('Детализация OPEX').classes(
#             'text-sm font-bold mb-2'
#         )

#         with ui.grid(columns=3).classes(
#             '''
#             w-full
#             text-xs
#             text-gray-400
#             border-b
#             border-[#1f2937]
#             pb-2
#             '''
#         ):
#             ui.label('Статья расходов')
#             ui.label('Сумма').classes('text-right')
#             ui.label('Доля').classes('text-right')

#         body_classes = (
#             'w-full overflow-y-auto overflow-x-hidden'
#             if has_vertical_scroll
#             else 'w-full overflow-hidden'
#         )
#         with ui.element('div').style(
#             f'height: {body_height}px;'
#         ).classes(body_classes):

#             for row in rows:
#                 share = (
#                     row['value'] / total * 100
#                     if total
#                     else 0
#                 )

#                 with ui.grid(columns=3).classes(
#                     '''
#                     w-full
#                     items-center
#                     py-3
#                     text-sm
#                     border-b
#                     border-[#141c28]
#                     '''
#                 ):
#                     ui.label(row['label']).classes(
#                         'truncate whitespace-nowrap'
#                     )

#                     ui.label(
#                         f"{row['value']:,.0f} ₽".replace(',', ' ')
#                     ).classes(
#                         'text-right font-semibold'
#                     )

#                     ui.label(
#                         f'{share:.1f}%'
#                     ).classes(
#                         'text-right text-gray-300'
#                     )

def render_opex_details(
    data: dict,
    visible_rows: int = 5,
    row_height: int = 48,
) -> None:

    labels = {
        'electricity_compensation': 'Электроэнергия',
        'rent_payment': 'Аренда',
        'operator_commission': 'Комиссия оператора',
        'service_maintenance': 'Сервисное обслуживание',
        'internet_and_connection': 'Интернет и связь',
        'insurance': 'Страхование',
        'other_expenses': 'Прочие расходы',
    }

    rows = [
        {
            'key': key,
            'label': label,
            'value': float(data.get(key, 0) or 0),
        }
        for key, label in labels.items()
    ]

    total = sum(r['value'] for r in rows)

    has_scroll = len(rows) > visible_rows
    body_height = min(len(rows), visible_rows) * row_height

    grid_style = (
        'display:grid;'
        'grid-template-columns: minmax(280px, 320px) 140px 140px;'
        'column-gap:20px;'
        'align-items:center;'
    )

    with ui.card().classes('''
        w-full
        h-full
        bg-[#101923]/90
        border border-[#1f2937]
        rounded-xl
        shadow-xl
        p-4
        text-white
    '''):

        ui.label('Детализация OPEX').classes(
            'text-sm font-bold mb-3'
        )

        # Заголовок
        with ui.element('div').style(grid_style).classes('''
            w-full
            text-xs
            text-gray-400
            border-b
            border-[#1f2937]
            pb-2
        '''):
            ui.label('Статья расходов')
            ui.label('Сумма').classes('text-right')
            ui.label('Доля').classes('text-right')

        body_classes = (
            'w-full overflow-y-auto overflow-x-hidden'
            if has_scroll
            else 'w-full overflow-hidden'
        )

        with ui.element('div').style(
            f'height:{body_height}px;'
        ).classes(body_classes):

            for row in rows:

                share = row['value'] / total * 100 if total else 0

                with ui.element('div').style(grid_style).classes('''
                    w-full
                    py-3
                    border-b
                    border-[#141c28]
                    text-sm
                '''):

                    ui.label(row['label']).classes(
                        'truncate'
                    )

                    ui.label(
                        f"{row['value']:,.0f} ₽".replace(',', ' ')
                    ).classes(
                        'text-right font-semibold'
                    )

                    ui.label(
                        f'{share:.1f}%'
                    ).classes(
                        'text-right text-gray-300'
                    )

        # # Итог
        # with ui.element('div').style(grid_style).classes('''
        #     w-full
        #     pt-3
        #     mt-2
        #     border-t
        #     border-[#1f2937]
        #     text-sm
        #     font-bold
        # '''):

        #     ui.label('Итого OPEX')

        #     ui.label(
        #         f"{total:,.0f} ₽".replace(',', ' ')
        #     ).classes(
        #         'text-right'
        #     )

        #     ui.label('100%').classes(
        #         'text-right text-green-400'
        #     )