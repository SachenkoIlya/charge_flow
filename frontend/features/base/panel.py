from abc import ABC, abstractmethod
from core.logger.logger import logger
from nicegui import app
# from frontend.components.apply_filters.apply import (
#     get_context_filters, 
#     get_page_filters
# )


class BasePanel(ABC):
    page_key = str
    container = None
    
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
        return {
            'company_id': context.get('company_id'),
        }

    def get_page_filters(self, page_key):
        page = app.storage.user.get('pages', {})
        return page.get(page_key)

    def apply_filters(self):
        context_filters = self.get_context_filters()
        page_filters = self.get_page_filters(self.page_key)
        self.company_id = context_filters.get('company_id')
        self.payload = page_filters
        logger.debug(
            f'page_filters: {page_filters}, '
            f'company_id: {self.company_id}'
        )
      
    async def refresh(self):
        if not self.container:
            return
        self.container.clear()
        with self.container:
            await self.render_content()
    
    async def on_date_change(self):
        self.apply_filters()
        # await self.load_data()
        await self.refresh()