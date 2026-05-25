from nicegui import ui


def metric_card(metric: dict):
    with ui.card().classes(
        """
            bg-[#101923]/90
            border border-[#1f2937]
            rounded-xl
            shadow-xl
            p-4
            text-white
            min-h-[120px]
        """
    ):
        with ui.row().classes('items-start gap-4'):
            with ui.element('div').classes(
                f"""
                    {metric["icon_bg"]}
                    w-12 h-12
                    rounded-xl
                    flex items-center justify-center 
                """
            ):
                ui.icon(metric['icon']).classes('text-white text-2xl')
            
            with ui.column().classes('gap-1'):
                ui.label(metric['title']).classes(
                    'text-sm text-white'
                )

                ui.label(metric['subtitle']).classes(
                    'text-xs text-gray-400'
                )
            ui.label(metric['value']).classes(
                'text-2xl font-bold mt-5'
            )

            ui.label(metric['delta']).classes(
                'text-sm text-green-400 mt-2'
            )
     