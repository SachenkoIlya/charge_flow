from frontend.features.control_panel.metrics import  render_metrics_list
from frontend.features.control_panel.charts import render_pie_chart
from frontend.features.control_panel.renders.hight import render_hight
from nicegui import ui

LEFT_WRAPPER_STYLE = 'flex: 2.5; min-width: 0; display: flex'
CARD_CLASSES = 'p-6 w-full'
CARD_STYLE = 'flex: 1'
MAIN_ROW_CLASSES = 'w-full justify-between items-end'
SEPARATOR_CLASSES = 'my-2 bg-blue-300 h-[2px]'
BOTTOM_ROW_CLASSES = 'w-full gap-3'


async def render_left(metrics: dict, chart: list[dict]):
    with ui.element('div').style(LEFT_WRAPPER_STYLE):
        with ui.card().classes(CARD_CLASSES).style(CARD_STYLE):
            await render_hight()

            with ui.row().classes(MAIN_ROW_CLASSES):
                with ui.column():
                    render_metrics_list(
                        metrics=metrics['main'],
                        size_label='2xl',
                        size_value='3xl',
                    )

            ui.separator().classes(SEPARATOR_CLASSES)

            with ui.row().classes(BOTTOM_ROW_CLASSES):
                render_metrics_list(metrics=metrics['secondary'])
                render_pie_chart(data=chart)