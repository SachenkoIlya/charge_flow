from nicegui import ui


def metric_card(metric: dict):
    with ui.card().classes(
        '''
        bg-[#101923]/90 border border-[#1f2937] rounded-xl shadow-xl
        p-3 text-white h-[105px] overflow-hidden
        '''
    ):
        with ui.row().classes('items-start gap-3'):
            with ui.element('div').classes(
                f'{metric["icon_bg"]} w-10 h-10 rounded-lg flex items-center justify-center shrink-0'
            ):
                ui.icon(metric['icon']).classes('text-white text-lg')

            with ui.column().classes('gap-0 min-w-0'):
                ui.label(metric['title']).classes('text-sm text-white font-semibold')
                ui.label(metric['subtitle']).classes('text-xs text-gray-400')

        ui.space()

        with ui.row().classes('w-full items-end justify-between'):
            ui.label(metric['value']).classes(
                f"{metric.get('value_class', 'text-xl')} font-bold leading-tight"
            )

            ui.label(metric['delta']).classes(
                'text-xs text-green-400 font-semibold text-right'
            )