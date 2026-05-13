from nicegui import ui, app
from fastapi import Request
from frontend.components.render_filters import render_filters


def logout():
    app.storage.user.clear()
    app.storage.user.pop('token', None)
    ui.navigate.to('/login')

async def get_header(
    request: Request, 
    drawer, 
    apply_filters,
    page_key,
    refresh,
    on_date_change,
    role
):
    with ui.header().classes(
               'h-20 z-[100] bg-gradient-to-r from-blue-200 to-blue-800 border-b border-blue-500 flex items-center'
    ):

        # 👉 ЕДИНЫЙ КОНТЕЙНЕР (важно!)
        with ui.row().classes('w-full max-w-[2000px] mx-auto px-6 items-center justify-between'):
            
            # 🔹 ЛЕВАЯ ЧАСТЬ
            with ui.row().classes('items-center gap-4'):
                ui.image('/media/opower_no_backgraunds.png')\
                    .classes('w-15 h-15 cursor-pointer')\
                        .on('click', lambda: ui.navigate.to('/control_panel'))
                
                ui.button(icon='menu', on_click=lambda: drawer.toggle())\
                    .props('flat color=blue').classes('!text-blue-700')

            with ui.row().classes('items-center gap-4'):
            #     ui.label('Компания').classes('text-blue-900')
                await render_filters(
                        apply_filters=apply_filters,
                        on_date_change=on_date_change,
                        request=request,
                        page_key=page_key,
                        refresh=refresh,
                        role=role
                    )
                ui.label('Контакты')\
                    .classes('text-white text-lg cursor-pointer hover:text-blue-100')\
                    .on('click', lambda: ui.navigate.to('/contacts'))
                ui.button(icon='logout',
                          on_click=logout)\
                        .props('flat color=white')