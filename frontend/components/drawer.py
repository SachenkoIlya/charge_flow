from nicegui import ui  

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