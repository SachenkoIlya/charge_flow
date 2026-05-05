from dataclasses import dataclass
from fastapi import Request
from frontend.components.header import  get_header
from frontend.components.drawer import get_drawer
from nicegui import ui, app
from datetime import datetime
from frontend.utils.utils import utils

from frontend.features.trends.components import (
    render_high_block, 
    render_midle_block, 
    dynamics_by_day_from_middle_render,
    render_visual_container
)
from frontend.features.trends.charts import (
    render_connector_types_chart, 
    render_revenue_chart, 
    render_daily_dynamics_chart, 
    render_sessions_chart
)

@dataclass
class Panel:
    user: dict
    request: Request
    endpoints_name: str = 'trends'
    page_key: str = 'trends'

  
    def __post_init__(self):
        self.data = None
        today = datetime.now().strftime("%d.%m.%Y")
        
        pages = app.storage.user.setdefault('pages', {})
        page_state = pages.setdefault(self.page_key, {
            'date_from': today,
            'date_to': today,
        })

        context = app.storage.user.setdefault('context', {})
        context.setdefault('company_id', None)

        app.storage.user['pages'] = pages
        app.storage.user['context'] = context

        self.payload = page_state
        self.company_id = context.get('company_id')
        utils.logger.debug(app.storage.user)
    
    def apply_filters(self):
        page = app.storage.user.get('pages', {})
        page_state = page.get(self.page_key)

        context = app.storage.user.get('context')
        utils.logger.debug(f"context: {context}")
        company_id = context.get('company_id')

        utils.logger.debug(f"page_stae: {page_state}, company_id: {company_id}".upper())

        self.company_id = company_id
        self.payload = page_state
    
    async def render(self):
        role = self.user.get('role')
        drawer = get_drawer(role=role)
        await get_header(drawer=drawer, role=role, request=self.request)
        with ui.element('div').classes('w-full max-w-[2000px] mx-auto px-7 mt-3') as self.container:
            await self.render_content()

    async def render_content(self):
        # min-height: 650px
        with ui.element('div').style(
            'display: flex; flex-direction: column; gap: 10px; width: 100%;'
        ):
            await self.render_high()
            await self.render_middle()
            await self.render_low()

    # тест
    async def render_high(self):
        with ui.element('div').classes(
            'w-full h-[300px] bg-white rounded-xl shadow-sm border border-gray-200 p-3 overflow-hidden'
        ):
            ui.label('REVENUE BLOCK').classes('text-sm')

            with ui.element('div').classes(
                'flex w-full h-[250px] gap-2 mt-1 items-stretch'
            ):
                render_high_block()



    async def render_middle(self):
        with ui.row().classes('w-full gap-2 items-stretch h-[260px]'):
            
            # левый блок
            with ui.element('div').classes(
                'flex-1 h-full bg-white rounded-xl shadow-sm border border-gray-200 p-3 overflow-hidden'
            ):
                ui.label('ЭНЕРГИЯ').classes('text-sm')

                with ui.row().classes('w-full h-[210px] gap-2 mt-1 items-stretch'):
                    render_midle_block()

            # правый блок
            with ui.element('div').classes(
                'flex-1 h-full bg-white rounded-xl shadow-sm border border-gray-200 p-3 overflow-hidden'
            ):
                with ui.row().classes('w-full items-center justify-between mb-1'):
                    ui.label('ДИНАМИКА ПО ДНЯМ').classes('text-sm font-semibold')

                with ui.element('div').classes('w-full h-[210px]'):
                    dynamics_by_day_from_middle_render()
                    
            
    async def render_low(self):
        ROW = 'grid grid-cols-4 gap-2 w-full h-[200px]'
        CARD = 'min-w-0 h-full bg-white rounded-xl shadow-sm border border-gray-200 p-3 overflow-hidden'

        STYLE_LABEL = 'text-sm font-semibold mb-1'
        STYLE_ELEMENT = 'w-full h-[170px]'
        PARAMS_ECHARTS = 'w-full h-full'
        CHART_CARD = 'min-w-0 h-full bg-white rounded-xl shadow-sm border border-gray-200 p-3 overflow-hidden flex flex-col'
        CHART_BOX = 'w-full flex-1 min-h-0'
        CHART_STYLE_LABEL = 'text-sm font-semibold mb-0'
        with ui.element('div').classes(ROW):
            render_visual_container(
                label='СРЕДНЕЕ',
                CARD=CARD,
                STYLE_LABEL=STYLE_LABEL,
            )

            with ui.element('div').classes(CHART_CARD):
                ui.label('СЕССИИ').classes(CHART_STYLE_LABEL)
                with ui.element('div').classes(CHART_BOX):
                    options = render_sessions_chart()
                    ui.echart(options).classes('w-full h-full')
            
            with ui.element('div').classes(CHART_CARD):
                ui.label('ТИПЫ КОННЕКТОРОВ').classes(CHART_STYLE_LABEL)
                with ui.element('div').classes(CHART_BOX):
                    options = render_connector_types_chart()
                    ui.echart(options).classes('w-full h-full')

            render_visual_container(
                label='ЭКСПЛУАТАЦИЯ',
                CARD=CARD,
                STYLE_LABEL=STYLE_LABEL,
            )