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

