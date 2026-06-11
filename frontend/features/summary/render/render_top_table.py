from nicegui import ui

from frontend.features.summary.render.tables_section import render_tables_section

def render_top_tables_dialog(rows, reversed_rows):
    dialog = ui.dialog()

    with dialog:
        with ui.card().classes(
            '''
            w-[1200px] max-w-[95vw]
            bg-[#071019]
            border border-[#1f2937]
            rounded-xl
            p-5
            text-white
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