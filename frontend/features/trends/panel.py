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
        with ui.element('div').classes('w-full max-w-[2000px] mx-auto px-7 mt-10') as self.container:
            await self.render_content()

    async def render_content(self):
        with ui.element('div').style('display: flex; gap: 15px; width: 100%; align-items: stretch; min-height: 650px'):
            await self.render_revenue()

    async def render_revenue(self):
        # контейнер
        with ui.element('div').classes(
            'w-full flex gap-4'
        ).style('min-height: 350px'):
            # левый блок под графие
            with ui.element('div').classes(
                'flex-[3] min-w-0 border-2 border-blue-400 rounded-lg p-4'
            ):
                ui.label('LEFT (chart 3/4)')
            
            # правый блок 
            with ui.element('div').classes(
               'flex-[1] border-2 border-green-400 rounded-lg p-4'
            ):
                ui.label('LEFT (chart 1/4)')