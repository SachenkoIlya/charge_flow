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
        
        with ui.element('div').classes(
            'w-full max-w-[2000px] mx-auto px-7 mt-10'
        ) as self.container:
            await self.render_content()

    async def render_content(self):
        # min-height: 650px
        with ui.element('div').style(
            'display: flex; gap: 15px; width: 100%; align-items: stretch; min-height: 650px'
        ):
            await self.render_high()
            await self.render_middle()
            await self.render_low()


    async def render_high(self):
        with ui.element('div').classes(
            'w-full bg-white rounded-xl shadow-sm border border-gray-200 p-5'
        ):
            ui.label('REVENUE BLOCK')

            with ui.element('div').classes(
                'flex w-full gap-4 mt-1 items-start'
            ):
                render_high_block()



    async def render_middle(self):
        with ui.row().classes('w-full gap-3 items-stretch'):
            # левый визуальный контейнер
            with ui.element('div').classes(
                'flex-1 min-h-[220px] bg-white rounded-xl shadow-sm border border-gray-200 p-5'
            ):
                ui.label('ЭНЕРГИЯ')
                with ui.row().classes('w-full gap-4 items-start'):
                    render_midle_block()
            with ui.element('div').classes(
                'flex-1  min-h-[220px] bg-white rounded-xl shadow-sm border border-gray-200 p-5'
            ):
                with ui.row().classes('w-full items-center justify-between mb-2'):
                    ui.label('ДИНАМИКА ПО ДНЯМ').classes('text-sm font-semibold')
                dynamics_by_day_from_middle_render()
                
            
    async def render_low(self):
        with ui.row().classes('w-full gap-3 items-stretch flex-wrap'):
            render_visual_container(label='ЭКСПЛУАТАЦИЯ')
            render_visual_container(
                label='СРЕДНЕЕ',
            )
            METRIC_CARD_CLASSES = (
                'flex-1 min-w-0 h-[80px] '
                'bg-white rounded-lg shadow-sm border border-gray-200 p-3'
            )
            with ui.element('div').classes(
                'flex-1 min-w-[300px] min-h-[180px] bg-white rounded-xl shadow-sm border border-gray-200 p-4'
                # METRIC_CARD_CLASSES
            ):
                ui.label('СЕССИИ').classes('text-sm font-semibold mb-2')
                options = render_sessions_chart()
                ui.echart(options).classes('w-full h-[150px]')

            with ui.element('div').classes(
                'flex-1 min-w-[300px] min-h-[180px] bg-white rounded-xl shadow-sm border border-gray-200 p-4'
                # METRIC_CARD_CLASSES
            ):
                ui.label('ТИПЫ КОННЕКТОРОВ').classes('text-sm font-semibold mb-2')
                options = render_connector_types_chart()
                ui.echart(options).classes('w-full h-[150px]')
            # 4. ЭКСПЛУАТАЦИЯ
            
            # with ui.element('div').classes(
            #     'flex-1 min-w-[300px] min-h-[180px] bg-white rounded-xl shadow-sm border border-gray-200 p-4'
            # ):
            #     ui.label('ЭКСПЛУАТАЦИЯ').classes('text-sm font-semibold mb-3')

            #     with ui.row().classes('w-full gap-2'):
            #         for title, value, color in [
            #             ('Доступность', '98%', 'text-green-500'),
            #             ('Простой', '2%', 'text-red-500'),
            #             ('Утилизация', '67%', 'text-gray-700'),
            #         ]:
            #             with ui.element('div').classes(
            #                 ' bg-white rounded-lg shadow-sm border border-gray-200 p-3'
            #             ):
            #                 ui.label(title).classes('text-xs text-gray-500')
            #                 ui.label(value).classes(f'text-lg font-bold {color}')