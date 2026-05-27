from nicegui import ui

def render_pnl_table(rows: list[dict]):
       with ui.card().classes(
        '''
        w-full mt-5 bg-[#101923]/90 border border-[#1f2937]
        rounded-xl shadow-xl p-4 text-white overflow-x-auto
        '''
    ):
        ui.label('P&L по станциям').classes('text-base font-bold mb-3')

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

        with ui.row().classes('min-w-[1400px] text-xs text-gray-400 border-b border-[#1f2937] pb-2'):
            for label, _ in columns:
                ui.label(label).classes('w-[90px] truncate')

        for row in rows:
            with ui.row().classes('min-w-[1400px] text-sm text-gray-200 py-2 border-b border-[#141c28]'):
                for label, key in columns:
                    cls = 'w-[90px] truncate'
                    if key == 'station':
                        cls = 'w-[170px] truncate'
                    if key == 'margin':
                        cls += ' text-green-400 font-semibold'
                    ui.label(row[key]).classes(cls)