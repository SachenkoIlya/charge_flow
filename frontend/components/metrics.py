from nicegui import ui

def get_metrics(metric: dict):
    label = metric.get('label', '')
    value = metric.get('value', '')
    suffix = metric.get('suffix', '')
    emoji = metric.get('emoji', '')
    color = metric.get('color', 'text-gray-900')

    text = f'{value} {suffix}'.strip()
    if emoji:
        text = f'{text} {emoji}'
    
    with ui.element('div').classes(
        'w-full flex-1 min-h-0 bg-white rounded-lg shadow-sm border border-gray-200 p-2 overflow-hidden'
    ):
        ui.label(label).classes('text-xs text-gray-500 leading-tight')
        ui.label(text).classes(f'text-base font-bold leading-tight {color}')
