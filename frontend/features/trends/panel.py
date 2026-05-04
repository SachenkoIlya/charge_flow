from dataclasses import dataclass
from fastapi import Request
from frontend.components.header import  get_header
from frontend.components.drawer import get_drawer
from nicegui import ui, app
from datetime import datetime
from frontend.utils.utils import utils



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
      # главный контейнер (весь блок revenue)
        with ui.element('div').classes(
              'w-full bg-white rounded-xl shadow-sm border border-gray-200 p-5'
        ):
            ui.label('REVENUE BLOCK')
            # внутреннее деление
            with ui.element('div').classes(
                'flex w-full gap-4 mt-1'
            ).style('min-height: 260px'):

                # левый — 3/4 (график)
                with ui.element('div').classes(
                    'flex-[3] min-w-0 border-2 border-blue-400 rounded-lg p-4'
                ):
                    ui.label('CHART 3/4')

                # правый — 1/4 (метрики)
                with ui.element('div').classes(
                    'flex-[1] border-2 border-green-400 rounded-lg p-4'
                ):
                    ui.label('METRICS 1/4')
    
    async def render_middle_block(self):
        with ui.row().classes('w-full gap-3 items-stretch'):
            with ui.element('div').classes(
                'flex-1  min-h-[220px] bg-white rounded-xl shadow-sm border border-gray-200 p-5'
            ):
                ui.label('ЭНЕРГИЯ')
            with ui.element('div').classes(
                'flex-1  min-h-[220px] bg-white rounded-xl shadow-sm border border-gray-200 p-5'
            ):
                ui.label('ДИНАМИКА ПО ДНЯМ')
    
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