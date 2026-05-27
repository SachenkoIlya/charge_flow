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


def render_plan_fact_table(title: str, rows: list[dict]):
    with ui.card().classes(
        '''
        bg-[#101923]/90 border border-[#1f2937]
        rounded-xl shadow-xl p-4 text-white
        '''
    ):

        ui.label(title).classes(
            'text-base font-bold mb-4 text-white'
        )

        with ui.grid(
            columns='1.4fr 1fr 1fr 1fr 70px'
        ).classes(
            'w-full text-xs text-gray-400 mb-2'
        ):

            ui.label('Показатель')
            ui.label('План')
            ui.label('Факт')
            ui.label('Отклонение')
            ui.label('%')

        for row in rows:

            color = (
                'text-green-400'
                if row['positive']
                else 'text-red-400'
            )

            with ui.grid(
                columns='1.4fr 1fr 1fr 1fr 70px'
            ).classes(
                '''
                w-full
                text-sm
                text-gray-200
                py-2
                border-t border-[#1f2937]
                items-center
                '''
            ):

                ui.label(row['metric']).classes(
                    'text-gray-300'
                )

                ui.label(row['plan'])

                ui.label(row['fact'])

                ui.label(row['delta']).classes(
                    color
                )

                ui.label(row['percent']).classes(
                    f'{color} font-semibold text-right'
                )