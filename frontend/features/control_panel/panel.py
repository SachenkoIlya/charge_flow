from frontend.features.control_panel.metrics import get_metrics, render_metrics_list
from frontend.features.control_panel.charts import render_pie_chart
from frontend.components.calendar import get_calendar
from frontend.components.header import get_header
from frontend.components.drawer import get_drawer
from frontend.api.client import universal_api
from frontend.components.stat_card import stat_card
from frontend.utils.utils import utils
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime

from nicegui import ui, app
from fastapi import Request



@dataclass
class Panel:
    user: dict
    request: Request
    endpoints_name: str = 'dashboard_stats'
    page_key = 'control_panel'
    
    
    def __post_init__(self):
        self.data = None
        
        context = app.storage.user.get('context', {})
        context.setdefault('company_id', None)
        app.storage.user['context'] = context

        
        today = datetime.now().strftime("$Y-$m-$d")
        page = app.storage.user.get('pages', {})
        page.setdefault(self.page_key)
        
        app.storage.user['pages'][self.page_key] = page
        utils.logger.debug(app.storage.user)


    async def refresh(self):
        self.container.clear()
        with self.container:
            await self.render_content()

    def apply_filters(self):
        page = app.storage.user.get('pages', {})
        page_state = page.get(self.page_key)

        context = app.storage.user.get('context')
        utils.logger.debug(f"context: {context}")
        company_id = context.get('company_id')

        utils.logger.debug(f"page_stae: {page_state}, company_id: {company_id}".upper())

        today = datetime.now().strftime('%d.%m.%Y')
        
        self.date_from = page_state.get('date_from') or today
        self.date_to = page_state.get('date_to') or self.date_from
        self.company_id = company_id
    
    
  
    async def on_date_change(self):
        self.apply_filters()
        await self.load_data()
        await self.refresh()

    async def render(self):
        self.apply_filters()
        await self.load_data()
        
        role = self.user.get('role')
        drawer = get_drawer(role=role)
        
        await get_header(
            drawer=drawer, 
            role=role, 
            on_company_change=self.on_date_change,
            request=self.request
            )
        
        with ui.element('div').classes('w-full max-w-[2000px] mx-auto px-7 mt-10') as self.container:
            await self.render_content()
    
    async def render_content(self):
        metrics = get_metrics(self.data)
        chart = self.data['chart']
        
        with ui.element('div').style('display: flex; gap: 15px; width: 100%; align-items: stretch; min-height: 650px'):
            await self.render_left(metrics, chart)
            await self.render_right(metrics)
            ...

    async def render_header(self):
        with ui.row().classes('w-full justify-between items-start'):
            # левая часть
            with ui.column().classes('gap-1 mb-10'):
                ui.label('Общий доход по всем локациям').classes('text-3xl font-semibold text-gray-800')
                ui.label('Агрегировано по всей сети станций').classes('text-l font-semibold text-gray-500')
                
            # правая часть
            with ui.column().classes('items-end'):
                await get_calendar(on_change_date=self.on_date_change, page_key=self.page_key)

    async def render_left(self, metrics: dict, chart: list[dict]):
        # p-6 w-full animate-[fadeInUp_0.5s_ease-out]
        with ui.element('div').style('flex: 2.5; min-width: 0; display: flex'):
            with ui.card().classes('p-6 w-full').style('flex: 1'):
                await self.render_header()
                # ui.space()
                with ui.row().classes('w-full justify-between items-end'):
                    with ui.column():
                        render_metrics_list(
                            metrics=metrics['main'],
                            size_label='2xl',
                            size_value='3xl'
                        )
                    # with ui.column().classes('items-end'):
                    #         await get_calendar(on_change_date=self.on_date_change)
                            # ui.label("тест, тут должа быть дата )").classes('text-xs text-gray-500 mt-1')
                ui.separator().classes('my-2 bg-blue-300 h-[2px]')

                with ui.row().classes('w-full gap-3'):
                    render_metrics_list(metrics=metrics['secondary'])
                    render_pie_chart(data=chart)
    

    async def render_right(self, metrics: dict):
        with ui.element('div').style('width: 30%; padding: 0;'):
            # with ui.element('div').style('flex: 1'):
                with ui.element('div').style('display: grid; grid-template-rows: repeat(4, 1fr); gap: 12px; height: 100%'):
                    for m in metrics['extra']:
                        stat_card(
                            label=m['label'],
                            value=m['value'],
                            gradient=m.get('color')
                        )


    async def load_data(self):
        payload = deepcopy(self.payload)
        
        if self.company_id:
            payload['company_id'] = self.company_id
        
        utils.logger.debug(payload)

        data = await universal_api(
            endpoint_name=self.endpoints_name,
            payloads=payload,
            request=self.request
        )
        
        if not data or data.get('error'):
            ui.notify('Сервер недоступен', color='red')
            return
            
        status_code = data['status_code']
        answer = data['data']

        if status_code == 401:
            ui.notify(answer.get('detail'), color='red')
            ui.navigate.to('/login')
            return

        if status_code == 403:
            ui.notify(answer.get('detail'), color='red')
            return

        if status_code >= 400:
            ui.notify(f'Ошибка: {status_code}', color='red')
            return

        self.data = answer