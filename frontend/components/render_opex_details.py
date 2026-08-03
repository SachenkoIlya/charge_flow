from nicegui import ui


def render_opex_details(data: dict) -> None:
    labels = {
        'electricity_compensation': 'Электроэнергия',
        'rent_payment': 'Аренда',
        'operator_commission': 'Комиссия оператора',
        'service_maintenance': 'Сервисное обслуживание',
        'internet_and_connection': 'Интернет и связь',
        'insurance': 'Страхование',
        'taxes': 'Налоги',
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

    with ui.card().classes(
        '''
        w-full
        h-full
        bg-[#101923]/90
        border border-[#1f2937]
        rounded-xl
        shadow-xl
        p-4
        text-white
        '''
    ):
        ui.label('Детализация OPEX').classes(
            'text-base font-bold mb-3'
        )

        with ui.grid(columns=3).classes(
            '''
            w-full
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

        for row in rows:
            share = (
                row['value'] / total * 100
                if total
                else 0
            )

            with ui.grid(columns=3).classes(
                '''
                w-full
                items-center
                py-3
                text-sm
                border-b
                border-[#141c28]
                '''
            ):
                ui.label(row['label']).classes(
                    'truncate whitespace-nowrap'
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

        with ui.grid(columns=3).classes(
            'w-full items-center pt-4'
        ):
            ui.label('Итого OPEX').classes(
                'font-bold'
            )

            ui.label(
                f'{total:,.0f} ₽'.replace(',', ' ')
            ).classes(
                'text-right text-base font-bold'
            )

            ui.label('100%').classes(
                'text-right font-semibold text-green-400'
            )