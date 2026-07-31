from nicegui import ui

def render_pnl_table(rows: list[dict], height:int=600):
        # h-[{height}px]
       with ui.card().classes(
        f'''
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
        # ui.label('P&L по станциям').classes('text-base font-bold mb-3')
        with ui.element('div').classes(
            'w-full overflow-x-auto'
        ):
            with ui.element('div').classes(
                'min-w-[1500px]'
            ):
                columns = [
                    ('Станция', 'station', 220),
                    ('Выручка мес.', 'revenue_month', 150),
                    ('Э/энергия ₽', 'energy_cost', 140),
                    ('кВт⋅ч', 'kwh', 110),
                    ('Аренда фикс.', 'rent_fixed', 130),
                    ('Аренда итого', 'rent_total', 140),
                    ('EBITDA', 'ebitda', 130),
                    ('Прибыль', 'profit', 130),
                    ('Маржа', 'margin', 100),
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
                    for label, _, width in columns:
                        ui.label(label).style(
                            f'width: {width}px'
                        ).classes(
                            'shrink-0 truncate whitespace-nowrap'
                        )

                for row in rows:
                    with ui.row().classes(
                        '''
                        min-w-[1400px]
                        text-sm text-gray-200
                        py-4
                        border-b border-[#141c28]
                        flex-nowrap
                        '''
                    ):
                        for _, key, width in columns:

                            cls = 'shrink-0 truncate whitespace-nowrap'

                            if key == 'margin':
                                cls += ' text-green-400 font-semibold'

                            ui.label(row[key]).style(
                                f'width: {width}px'
                            ).classes(cls)