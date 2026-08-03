from nicegui import ui

def render_opex_details(
    data: dict,
    visible_rows: int = 3,
    row_height: int = 44,
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

    total = sum(row['value'] for row in rows)
    body_height = min(len(rows), visible_rows) * row_height

    grid_style = (
        'display: grid; '
        'grid-template-columns: minmax(260px, 1fr) 180px 90px; '
        'column-gap: 24px;'
    )

    with ui.card().classes(
        '''
        w-full
        bg-[#101923]/90
        border border-[#1f2937]
        rounded-xl
        shadow-xl
        p-4
        text-white
        overflow-hidden
        '''
    ):
        ui.label('Детализация OPEX').classes(
            'text-sm font-bold mb-2'
        )

        # Шапка таблицы
        with ui.element('div').style(grid_style).classes(
            '''
            w-full
            items-center
            text-xs
            text-gray-400
            border-b
            border-[#1f2937]
            pb-2
            '''
        ):
            ui.label('Статья расходов')
            ui.label('Сумма').classes('text-right')
            ui.label('Доля').classes('text-right')

        # Тело таблицы
        with ui.element('div').style(
            f'height: {body_height}px;'
        ).classes(
            '''
            w-full
            overflow-y-auto
            overflow-x-hidden
            '''
        ):
            for row in rows:
                share = (
                    row['value'] / total * 100
                    if total
                    else 0
                )

                with ui.element('div').style(
                    grid_style + f' min-height: {row_height}px;'
                ).classes(
                    '''
                    w-full
                    items-center
                    text-sm
                    border-b
                    border-[#141c28]
                    hover:bg-[#16212d]
                    transition-colors
                    '''
                ):
                    ui.label(row['label']).classes(
                        'truncate whitespace-nowrap'
                    )

                    ui.label(
                        f"{row['value']:,.0f} ₽".replace(',', ' ')
                    ).classes(
                        'text-right font-semibold whitespace-nowrap'
                    )

                    ui.label(
                        f'{share:.1f}%'
                    ).classes(
                        'text-right text-gray-300 whitespace-nowrap'
                    )

        # Итоговая строка
        with ui.element('div').style(grid_style).classes(
            '''
            w-full
            items-center
            pt-3
            mt-1
            text-sm
            '''
        ):
            ui.label('Итого OPEX').classes(
                'font-bold'
            )

            ui.label(
                f'{total:,.0f} ₽'.replace(',', ' ')
            ).classes(
                'text-right font-bold whitespace-nowrap'
            )

            ui.label('100%').classes(
                'text-right font-semibold text-green-400'
            )