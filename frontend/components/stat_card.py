from nicegui import ui


def stat_card(label, value, gradient: str=None):
    with ui.card().classes(
        f'w-full p-6 rounded-xl shadow-sm bg-gradient-to-r {gradient} border border-gray-200'
    ):
        ui.label(label).classes('text-xl font-semibold text-gray-700')
        ui.label(value).classes('text-2xl font-bold text-gray-900 mt-2')