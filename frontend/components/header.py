from nicegui import ui, app
from fastapi import Request
from frontend.features.dashboard.charts import (
    get_filtered_company_from_admin, 
)


def logout():
    app.storage.user.clear()
    app.storage.user.pop('token', None)
    ui.navigate.to('/login')

async def get_header(request: Request, drawer, role: str, on_company_change=None, render_filters=None):
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

                with ui.row().classes('gap-3 items-center'):
                    # get_calendar()
                    if role == 'admin':
                        await get_filtered_company_from_admin(request=request, on_change=on_company_change)
            # Правая часть
            with ui.row().classes('items-center gap-4'):
            #     ui.label('Компания').classes('text-blue-900')
                if render_filters:
                    await render_filters()
                ui.label('Контакты')\
                    .classes('text-white text-lg cursor-pointer hover:text-blue-100')\
                    .on('click', lambda: ui.navigate.to('/contacts'))
                ui.button(icon='logout',
                          on_click=logout)\
                        .props('flat color=white')