from nicegui import ui


def render_top_table(title: str, title_class: str, rows: list):
    with ui.card().classes(
        '''
        bg-[#101923]/90 border border-[#1f2937]
        rounded-xl shadow-xl p-4 text-white
        '''
    ):
        ui.label(title).classes(f'text-base font-bold mb-4 {title_class}')

        with ui.grid(columns='40px 1fr 100px 90px').classes(
            'w-full text-xs text-gray-400 mb-2'
        ):
            ui.label('#')
            ui.label('Станция')
            ui.label('Выручка, ₽')
            ui.label('Загрузка, %')

        for i, row in enumerate(rows, start=1):
            with ui.grid(columns='40px 1fr 100px 90px').classes(
                'w-full text-sm text-gray-200 py-2 border-t border-[#1f2937]'
            ):
                ui.label(str(i)).classes('text-gray-400')
                ui.label(row['station'])
                ui.label(row['revenue'])
                ui.label(row['load'])

TOP_ROWS = [
    {'station': 'ЭЭС-105 ТЦ Мега Химки', 'revenue': '1 245 780', 'load': '38.6%'},
    {'station': 'ЭЭС-042 ТРК Европолис', 'revenue': '1 102 430', 'load': '35.2%'},
    {'station': 'ЭЭС-089 ТЦ Афимолл Сити', 'revenue': '1 087 950', 'load': '34.7%'},
    {'station': 'ЭЭС-077 ТЦ Калейдоскоп', 'revenue': '986 210', 'load': '32.1%'},
    {'station': 'ЭЭС-021 Аэропорт Шереметьево', 'revenue': '872 340', 'load': '29.8%'},
]


REVERS_ROWS = list(reversed(TOP_ROWS))
