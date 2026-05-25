from nicegui import ui


def metric_card(metric: dict):
    with ui.card().classes(
        """
            bg-[#101923]/90
            border border-[#1f2937]
            rounded-xl
            shadow-xl
            p-3
            text-white
            h-[105px]
        """
    ):
        with ui.row().classes('items-start gap-3'):
            with ui.element('div').classes(
                f"""
                    {metric["icon_bg"]}
                    w-10 h-10
                    rounded-lg
                    flex items-center justify-center
                """
            ):
                ui.icon(metric['icon']).classes('text-white text-lg')
            
            with ui.column().classes('gap-1'):
                ui.label(metric['title']).classes(
                    'text-sm text-white'
                )

                ui.label(metric['subtitle']).classes(
                    'text-xs text-gray-400'
                )
            ui.label(metric['value']).classes(
                'text-xl font-bold mt-3'
            )

            ui.label(metric['delta']).classes(
                'text-sm text-green-400 mt-1'
            )
     