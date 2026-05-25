from nicegui import ui, app  



def logout():
    app.storage.user.clear()
    app.storage.user.pop('token', None)
    ui.navigate.to('/login')

def get_drawer(role: str) -> ui.left_drawer:
    def nav_item(icon, text, route):
        with ui.row().classes(
            'flex items-center gap-3 px-4 py-3 rounded-xl font-semibold '
            'text-gray-800 hover:bg-gray-100 cursor-pointer transition'
        ).on('click', lambda: ui.navigate.to(route)):
            ui.icon(icon, size='20px')
            ui.label(text)

    with ui.left_drawer().props(
        'overlay behavior=mobile bordered'
        # 'overlay behavior=mobile show-if-above=false elevated bordered'
    ).classes('z-10').style('background-color: #ebf1fa') as drawer:

        drawer.value = False
        
        nav_item('trending_up', 'Тренды', '/trends')
        if role == 'admin':
            with ui.column().classes('gap-1 pg-4'):
                nav_item('groups', 'Инвесторы', '/investors')
                ui.separator()
                nav_item('link', 'Подключить оператора', '/operator')
                nav_item('link', 'Мониторинг системы', '/system_monitoring')
                

        else:
            nav_item('ev_station', 'Мои станции', '/stations')
            nav_item('bar_chart', 'Аналитика', '/analytics')
        ui.query('.q-drawer').style('top: 80px')
        ui.query('.q-drawer').style('height: calc(100% - 80px)')

    return drawer





def render_sidebar(role: str):
    def nav_item(icon, text, route, active=False):
        with ui.row().classes(
            f"""
            w-full items-center gap-3 px-4 py-3 rounded-xl font-semibold
            cursor-pointer transition
            {'bg-[#122033] text-white' if active else 'text-gray-300 hover:bg-[#111827] hover:text-white'}
            """
        ).on('click', lambda: ui.navigate.to(route)):
            ui.icon(icon, size='20px')
            ui.label(text)

    with ui.column().classes(
        """
        w-[260px] min-h-screen shrink-0
        bg-[#071019]
        border-r border-[#1f2937]
        px-4 pt-8 gap-2
        """
    ):
        ui.label('Панель').classes('text-xl font-bold text-white mb-4')

        nav_item('dashboard', 'Общая сводка', '/control_panel', active=True)
        nav_item('dashboard', 'Сводка', '/summary', active=False)
        nav_item('trending_up', 'Тренды', '/trends')

        if role == 'admin':
            nav_item('groups', 'Инвесторы', '/investors')
            ui.separator().classes('bg-[#1f2937] my-2')
            nav_item('link', 'Подключить оператора', '/operator')
            nav_item('monitor_heart', 'Мониторинг системы', '/system_monitoring')
        else:
            nav_item('ev_station', 'Мои станции', '/stations')
            nav_item('bar_chart', 'Аналитика', '/analytics')

        ui.space()
        nav_item('contacts', 'Контакты', '/contacts')
        with ui.row().classes(
        '''
            w-full items-center gap-3 px-4 py-3 rounded-xl font-semibold
            cursor-pointer transition text-gray-300 hover:bg-[#111827] hover:text-white
        '''
        ).on('click', logout):
            ui.icon('logout', size='20px')
            ui.label('Выйти')