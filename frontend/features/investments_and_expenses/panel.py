from dataclasses import dataclass
from fastapi import Request
from frontend.components.drawer import render_sidebar
from frontend.components.render_title import get_data_from_map, render_title
from frontend.features.base.panel import BasePanel
from nicegui import ui, app
from core.logger.logger import logger
from copy import deepcopy

from frontend.features.investments_and_expenses.render.form import (
    EXPENSES_MAP, 
    SELECTED_STATION, 
    render_form
)


@dataclass
class Panel(BasePanel):
    user: dict
    request: Request
    endpoints_name: str = 'investments'
    page_key = 'investments_and_expenses'

    async def render_content(self):
        
        page = app.storage.user.get('pages', {})
        page_state = page.get(self.page_key, {})
        toggle_value = page_state.get('toggle_value', 'capex')
        
        with ui.element('div').style('zoom: 1'):
            await render_title(
                label='Инвестиционные и операционные расходы',
                # label_aggre='Инвестиции и операционные расходы',
                page_key=self.page_key,
                on_date_change=self.on_date_change 
            )
            
            logger.debug(f"перед render_form {self.page_key} проверяем")
            logger.debug(f"toggle_value = {toggle_value}")
            await render_form(
                request=self.request,
                data=EXPENSES_MAP, 
                selected_station=self.stations,
                mode=toggle_value.lower()
                )
            
   

        