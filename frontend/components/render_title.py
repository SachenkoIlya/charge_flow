from nicegui import ui

from frontend.components.calendar import get_calendar


async def render_title(
    label: str, 
    label_aggre: str,
    page_key: str,
    on_date_change=None,

):
    with ui.row().classes('w-full items-start justify-between mb-6'):

        with ui.column().classes('gap-0'):
            ui.label(label).classes(
                'text-3xl font-bold text-white leading-tight'
            )

            ui.label(label_aggre).classes(
                'text-sm text-gray-400 mt-1'
            )

        if page_key in {'finance'}:

            selected = {'value': 'ВСЕ'}
            with ui.row().classes(
                '''
                items-center gap-1
                bg-[#101923]
                border border-[#1f2937]
                rounded-2xl
                p-1
                '''
                
            ):
                buttons = {}
                def set_active(value):
                    selected['value'] = value

                    for key, btn in buttons.items():

                        if key == value:
                            btn.classes(
                                replace=
                                '''
                                px-5 py-2.5
                                rounded-xl
                                text-sm font-bold
                                bg-green-500
                                text-black
                                transition
                                '''
                            )

                    else:
                        btn.classes(
                            replace=
                                '''
                                px-5 py-2.5
                                rounded-xl
                                text-sm font-bold
                                text-gray-300
                                hover:bg-[#1a2432]
                                hover:text-white
                                transition
                                '''
                        )
                for item in ['6 МЕС', '1 ГОД', 'ВСЕ']:
                    btn = ui.button(
                        item,
                        on_click=lambda v=item: set_active(v)
                    ).props('flat')

                    buttons[item] = btn
                set_active('ВСЕ')
        else:
            await get_calendar(
                page_key=page_key,
                on_change_date=on_date_change,
            )
    