from nicegui import ui
from frontend.features.summary.render.metrics import METRICS, get_metric_value, get_metric_delta

def render_metrics(data: dict, columns:int):
    
    with ui.grid(columns=columns).classes(
        'w-full gap-4 mt-6'
    ):
        for metric in METRICS:
            key = metric.get('key', '')
            value = get_metric_value(key, data)
            delta = get_metric_delta(key, data)
            metric_card(metric, value, delta)




def metric_card(metric: dict, value:str, delta:str):
    with ui.card().classes(
        '''
        bg-[#101923]/90 border border-[#1f2937] rounded-xl shadow-xl
        p-3 text-white h-[105px] overflow-hidden
        '''
    ):
        with ui.row().classes(
            # 'items-start gap-3'
            'items-start gap-3 w-full overflow-hidden'
        ):
            with ui.element('div').classes(
                f'{metric["icon_bg"]} w-10 h-10 rounded-lg flex items-center justify-center shrink-0'
            ):
                ui.icon(metric['icon']).classes('text-white text-lg')

            with ui.column().classes(
                # 'gap-0 min-w-0'
                'gap-0 min-w-0 flex-1'
            ):
                ui.label(metric['title']).classes('text-sm text-white font-semibold')
                ui.label(metric['subtitle']).classes('text-xs text-gray-400')

        # ui.space()

        with ui.row().classes('w-full items-end justify-between'):
            ui.label(metric[value]).classes(
                f"{metric.get('value_class', 'text-xl')} font-bold leading-tight"
            )
            ui.label(metric[delta]).classes(
                'text-xs text-green-400 font-semibold text-right'
            )