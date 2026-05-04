from dataclasses import dataclass
from fastapi import Request
from frontend.components.header import  get_header
from frontend.components.drawer import get_drawer
from nicegui import ui, app
from datetime import datetime
from frontend.utils.utils import utils
from frontend.features.trends.charts import render_revenue_chart, render_daily_dynamics_chart


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
            await self.render_revenue()
            await self.render_middle_block()
            await self.render_low_block()


    async def render_revenue(self):
        with ui.element('div').classes(
            'w-full bg-white rounded-xl shadow-sm border border-gray-200 p-5'
        ):
            ui.label('REVENUE BLOCK')

            with ui.element('div').classes(
                'flex w-full gap-4 mt-1 items-start'
            ):
                # левый — 3/4
                with ui.element('div').classes(
                      'flex-[3] min-w-0 border-2 border-blue-400 rounded-lg p-4'
                ):
                    ui.label('CHART 3/4')
                    options = render_revenue_chart()
                    ui.echart(options).classes('w-full h-[240px]')
                # правый — 1/4
                with ui.element('div').classes(
                    'flex-[1] border-2 border-green-400 rounded-lg p-4'
                ):
                    ui.label('METRICS 1/4')

                    with ui.column().classes('w-full gap-2 mt-3'):
                        with ui.element('div').classes(
                            'w-full bg-white rounded-lg shadow-sm border border-gray-200 p-3'
                        ):
                            ui.label('Текущий год').classes('text-xs text-gray-500')
                            ui.label('1 863 000 ₽').classes('text-lg font-bold')

                        with ui.element('div').classes(
                            'w-full bg-white rounded-lg shadow-sm border border-gray-200 p-3'
                        ):
                            ui.label('Прошлый год').classes('text-xs text-gray-500')
                            ui.label('1 540 000 ₽').classes('text-lg font-bold')

                        with ui.element('div').classes(
                            'w-full bg-white rounded-lg shadow-sm border border-gray-200 p-3'
                        ):
                            ui.label('Рост (YoY)').classes('text-xs text-gray-500')
                            ui.label('+12% ↗').classes('text-lg font-bold text-green-500')

    async def render_middle_block(self):
        with ui.row().classes('w-full gap-3 items-stretch'):
            # левый визуальный контейнер
            with ui.element('div').classes(
                'flex-1 min-h-[220px] bg-white rounded-xl shadow-sm border border-gray-200 p-5'
            ):
                ui.label('ЭНЕРГИЯ')

                with ui.row().classes('w-full gap-4 items-start'):

                # график слева
                    with ui.element('div').classes(
                        'flex-[2] min-w-0 border-2 border-blue-400 rounded-lg p-3'
                    ):
                        options = render_revenue_chart()
                        ui.echart(options).classes('w-full h-[220px]')

                    # метрики справа
                    with ui.column().classes('flex-[1] gap-3 h-full justify-between'):
                        with ui.element('div').classes(
                            'w-full bg-white rounded-lg shadow-sm border border-gray-200 p-3'
                        ):
                            ui.label('Текущий год').classes('text-xs text-gray-500')
                            ui.label('93 000 кВт⋅ч').classes('text-lg font-bold')

                        with ui.element('div').classes(
                            'w-full bg-white rounded-lg shadow-sm border border-gray-200 p-3'
                        ):
                            ui.label('Прошлый год').classes('text-xs text-gray-500')
                            ui.label('80 000 кВт⋅ч').classes('text-lg font-bold')

                        with ui.element('div').classes(
                            'w-full bg-white rounded-lg shadow-sm border border-gray-200 p-3'
                        ):
                            ui.label('Рост (YoY)').classes('text-xs text-gray-500')
                            ui.label('+16% ↗').classes('text-lg font-bold text-green-500')
                        
            # второй визуальный контейнер
            with ui.element('div').classes(
                'flex-1  min-h-[220px] bg-white rounded-xl shadow-sm border border-gray-200 p-5'
            ):
                with ui.row().classes('w-full items-center justify-between mb-2'):
                    ui.label('ДИНАМИКА ПО ДНЯМ').classes('text-sm font-semibold')

                options = render_daily_dynamics_chart()
                ui.echart(options).classes('w-full h-[240px]')
    
    
    async def render_low_block(self):
        with ui.row().classes('w-full gap-3 items-stretch'):
            with ui.element('div').classes(
                'flex-1  min-h-[180px] bg-white rounded-xl shadow-sm border border-gray-200 p-5'
            ):
                ui.label('СРЕДНЕЕ ПО ДНЮ')
            
            with ui.element('div').classes(
                'flex-1  min-h-[180px] bg-white rounded-xl shadow-sm border border-gray-200 p-5'
            ):
                ui.label('СЕССИИ')
            with ui.element('div').classes(
                'flex-1  min-h-[180px] bg-white rounded-xl shadow-sm border border-gray-200 p-5'
            ):
                ui.label('ТИПЫ КОННЕКТОРОВ')