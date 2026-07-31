from abc import ABC, abstractmethod
from core.logger.logger import logger
from nicegui import app
from datetime import datetime
from copy import deepcopy

from frontend.api.client import frontend_api
from frontend.components.drawer import render_sidebar
from frontend.components.get_station import _get_selected_station
from frontend.components.render_title import get_data_from_map
from nicegui import ui
from typing import ClassVar

class BasePanel(ABC):
    user: dict
    page_key: str
    endpoints_name: str
    stations: dict[int, str] = {}
    container = None

    content_scale: ClassVar[float] = 0.92
    
    def __post_init__(self):

        self.data = None
        today = datetime.now().strftime("%d.%m.%Y")

        pages = app.storage.user.setdefault('pages', {})
        page_state = pages.setdefault(self.page_key, {
            # 'date_from': today,
            # 'date_to': today,
            'station_ids': [],
            'toggle_value': None
        })

        context = app.storage.user.setdefault('context', {})
        context.setdefault('company_id', None)

        app.storage.user['pages'] = pages
        app.storage.user['context'] = context

        self.payload = page_state
        self.company_id = context.get('company_id')
  
    # def reset_page_dates(self):
    #     today = datetime.now().strftime("%d.%m.%Y")
    #     pages = app.storage.user.setdefault('pages', {})
    #     page_state = pages.setdefault(self.page_key, {})
    #     page_state['date_from'] = today
    #     page_state['date_to'] = today

    #     app.storage.user['pages'] = pages
    
    @abstractmethod
    async def render_content(self):
        """
        Render page-specific dashboard content.

        Must be implemented in child panel classes.
        """
        raise NotImplementedError(
            'render_content() must be implemented in child panel'
        )
    
    def get_context_filters(self):
        context = app.storage.user.get('context')
        return context

    def get_page_filters(self, page_key):
        page = app.storage.user.get('pages', {})
        return page.get(page_key)

    def apply_filters(self):
        context_filters = self.get_context_filters()
        page_filters = self.get_page_filters(self.page_key)
        self.company_id = context_filters.get('company_id')
        self.payload = page_filters
        
    async def load_station(self) -> None:
        if self.stations:
            return
        self.stations = await _get_selected_station(self.request)

    async def refresh(self):
        if not self.container:
            return
        self.container.clear()
        with self.container:
            await self.render_content()
    
    async def on_date_change(self):
        self.apply_filters()
        loaded = await self.load_data()
        if loaded:
            await self.refresh()
    
    async def load_data(self):
        if self.endpoints_name == 'investments':
            return True
        
        if self.page_key in {'finance', 'system', 'summary'}:
            payload = {
                'period': self.payload.get('toggle_value'),
                'station_ids': self.payload.get('station_ids')
            }
        else:
            payload = deepcopy(self.payload)
        
        logger.debug(f"{self.page_key}: зашли в load_data".upper())
        logger.debug(f"payload: {payload}")
        
        response = await frontend_api(
            endpoint_name=self.endpoints_name,
            payloads=payload,
            request=self.request
        )
        if response is None:
            self.data = {}
            return False
        self.data = response
        return True

    async def get_selected_stations(self):
        return await _get_selected_station(self.request)
    
    async def render(self):
        await self.load_station()
        
        page = app.storage.user.setdefault('pages', {})
        page_state = page.setdefault(self.page_key, {})
                
        data = get_data_from_map(self.page_key)

        if data and page_state.get('toggle_value') is None:
            page_state['toggle_value'] = data['default_value']
               
        self.apply_filters()
        loaded = await self.load_data()
        if not loaded:
            return
                
        role = self.user.get('role')
        
        with ui.element('div').classes(
            """
                w-screen
                h-screen
                flex
                bg-gradient-to-br
                from-[#050b12]
                via-[#08111b]
                to-[#0b1724]
                text-white
                overflow-hidden
            """
        ):
            render_sidebar(role=role)
        
            with ui.element('main').classes(
                """
                flex-1
                h-screen
                overflow-hidden
                px-10
                py-2
                """
            ) as self.container:
                with ui.element('div').classes(
                    'w-full h-full'
                ).style(
                    f'zoom: {self.content_scale};'
                ):
                    await self.render_content()


  