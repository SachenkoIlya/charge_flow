from nicegui import ui
from frontend.features.trends.config import config
from frontend.features.trends.components import render_visual_container
from frontend.features.trends.charts import (
    render_connector_types_chart, 
    render_sessions_chart
)    



async def render_low():
       
    with ui.element('div').classes(config.ROW):
        render_visual_container(
            label='СРЕДНЕЕ',
            CARD=config.CARD,
            STYLE_LABEL=config.STYLE_LABEL,
        )

        with ui.element('div').classes(config.CHART_CARD):
            ui.label('СЕССИИ').classes(config.CHART_STYLE_LABEL)
            with ui.element('div').classes(config.CHART_BOX):
                options = render_sessions_chart()
                ui.echart(options).classes('w-full h-full')
            
        with ui.element('div').classes(config.CHART_CARD):
            ui.label('ТИПЫ КОННЕКТОРОВ').classes(config.CHART_STYLE_LABEL)
            with ui.element('div').classes(config.CHART_BOX):
                options = render_connector_types_chart()
                ui.echart(options).classes('w-full h-full')

        render_visual_container(
            label='ЭКСПЛУАТАЦИЯ',
            CARD=config.CARD,
            STYLE_LABEL=config.STYLE_LABEL,
        )