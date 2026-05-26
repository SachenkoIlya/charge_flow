from nicegui import ui


def render_top_table(title: str, title_class: str, rows: list):
    with ui.card().classes(
        '''
        bg-[#101923]/90
        border border-[#1f2937]
        rounded-xl
        shadow-xl
        p-4
        text-white
        h-[260px]
        '''
    ):

        ui.label(title).classes(
            f'text-sm font-bold mb-3 {title_class}'
        )

        # header
        with ui.element('div').classes(
            'grid w-full text-xs text-gray-500 pb-2 border-b border-[#1f2937]'
        ).style(
            'grid-template-columns: 35px 1fr 110px 90px;'
        ):

            ui.label('#')
            ui.label('Станция')
            ui.label('Выручка')
            ui.label('Загрузка')

        # rows
        for i, row in enumerate(rows, start=1):

            with ui.element('div').classes(
                'grid w-full text-sm text-gray-200 py-2 border-b border-[#141c28] items-center'
            ).style(
                'grid-template-columns: 35px 1fr 110px 90px;'
            ):

                ui.label(str(i)).classes(
                    'text-gray-500'
                )

                ui.label(row['station']).classes(
                    'truncate'
                )

                ui.label(row['revenue']).classes(
                    'text-right'
                )

                ui.label(row['load']).classes(
                    'text-right'
                )

TOP_ROWS = [
    {'station': 'ЭЭС-105 ТЦ Мега Химки', 'revenue': '1 245 780', 'load': '38.6%'},
    {'station': 'ЭЭС-042 ТРК Европолис', 'revenue': '1 102 430', 'load': '35.2%'},
    {'station': 'ЭЭС-089 ТЦ Афимолл Сити', 'revenue': '1 087 950', 'load': '34.7%'},
    {'station': 'ЭЭС-077 ТЦ Калейдоскоп', 'revenue': '986 210', 'load': '32.1%'},
    {'station': 'ЭЭС-021 Аэропорт Шереметьево', 'revenue': '872 340', 'load': '29.8%'},
]