from nicegui import ui

def render_pnl_table(rows: list[dict]):
       with ui.card().classes(
        '''
            w-full
            h-[210px]
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
                columns = [
                    ('Станция', 'station'),
                    ('Выручка мес.', 'revenue_month'),
                    ('Выручка накоп.', 'revenue_total'),
                    ('Э/энергия ₽', 'energy_cost'),
                    ('кВт⋅ч', 'kwh'),
                    ('₽/кВт⋅ч', 'price_kwh'),
                    ('Аренда фикс.', 'rent_fixed'),
                    ('% от ТО', 'rent_percent'),
                    ('Аренда итого', 'rent_total'),
                    ('Комиссия своя', 'operator_own'),
                    ('Комиссия сторон.', 'operator_external'),
                    ('Комиссия всего', 'operator_total'),
                    ('% от ТО', 'operator_percent'),
                    ('EBITDA', 'ebitda'),
                    ('Прибыль', 'profit'),
                    ('Маржа', 'margin'),
                ]

                with ui.row().classes(
                    '''
                    min-w-[1400px]
                    text-xs text-gray-400
                    border-b border-[#1f2937]
                    pb-2
                    flex-nowrap
                    '''
                ):
                    for label, _ in columns:
                        ui.label(label).classes(
                            'w-[180px] shrink-0 truncate whitespace-nowrap'
                        )

                for row in rows:
                    with ui.row().classes(
                        '''
                        min-w-[1400px]
                        text-sm text-gray-200
                        py-2
                        border-b border-[#141c28]
                        flex-nowrap
                        '''
                    ):

                        for label, key in columns:

                            cls = 'w-[180px] shrink-0 truncate whitespace-nowrap'

                            if key == 'station':
                                cls = 'w-[180px] shrink-0 truncate whitespace-nowrap'

                            if key == 'margin':
                                cls += ' text-green-400 font-semibold'

                            ui.label(row[key]).classes(cls)