from nicegui import ui

from frontend.features.summary.render.tables_section import render_tables_section

def render_top_tables_dialog(rows, reversed_rows):
    dialog = ui.dialog()

    with dialog:
        with ui.card().classes(
            '''
            w-[68vw]
            max-w-[1350px]
            min-w-[1000px]
            bg-[#071019]
            border border-[#1f2937]
            rounded-2xl
            p-5
            text-white
            shadow-2xl
            '''
        ):
            with ui.row().classes('w-full items-center justify-between mb-4'):
                ui.label('Рейтинг станций').classes('text-xl font-bold text-white')

                ui.button(
                    icon='close',
                    on_click=dialog.close,
                ).props('flat dense round color=grey')

            render_tables_section(rows, reversed_rows)

    return dialog