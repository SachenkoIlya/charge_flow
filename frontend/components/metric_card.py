from nicegui import ui
from frontend.features.summary.render.metrics import METRICS, get_delta_class, get_metric_value, get_metric_delta
from typing import Any


def render_metrics(
    data: dict, 
    columns:int, 
    default_metrics:dict, 
    metric_value_func: Any, 
    metric_delta_func: Any, 
    on_top_click=None):
    with ui.grid(columns=columns).classes(
        'w-full gap-6 mt-3'
    ):
        for metric in default_metrics:
            key = metric.get('key', '')
            value = metric_value_func(key, data)
            delta = metric_delta_func(key, data)
            metric_card(
                metric, 
                value, 
                delta,
                on_details_click=on_top_click if key == 'total_revenue' else None,
            )


def metric_card(metric: dict, value:str, delta:str, on_details_click=None):
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
            if on_details_click:
                ui.icon('leaderboard').classes(
                '''
                cursor-pointer
                text-gray-400
                hover:text-white
                text-lg
                '''
            ).on(
                'click',
                lambda: on_details_click()
            )
        # ui.space()

        with ui.row().classes('w-full items-end justify-between'):
            ui.label(value).classes(
                f"{metric.get('value_class', 'text-xl')} font-bold leading-tight"
            )
            if metric['key'] not in {'stations'}:
                ui.label(delta).classes(
                    f'text-xs font-semibold text-right {get_delta_class(delta)}'
                )