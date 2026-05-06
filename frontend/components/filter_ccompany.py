from nicegui import ui, app
from frontend.utils.utils import utils
from frontend.api.client import universal_api
from fastapi import Request 
import asyncio 

selected_station = ['Все станции', 'Станция 1', 'Станция 2']

async def load_data(request:Request, endpoint_name:str):
    
    data = await universal_api(
        endpoint_name=endpoint_name,
        request=request,

    )
    if not data or data.get('error'):
        return 
            
    status_code = data['status_code']
    answer = data['data']
    
    if status_code == 403:
        ui.notify(answer.get('detail'), color='red')
        return 
    if status_code >= 402:
        ui.notify(f'Ошибка: {status_code}', color='red')
        return 
    return {item['id']: item['name'] for item in answer}




async def get_filtered_data(
        request: Request, 
        data: dict = None, 
        label:str=None,
        on_change=None,
        endpoint_name: str=None,
        page_key: str=None
    ):
    if not data:
        data = await load_data(
            request=request, 
            endpoint_name=endpoint_name
        )
    if endpoint_name in {'company'}:
        value = app.storage.user\
            .get('context', {})\
            .get(f'{endpoint_name}_id', None)
        
    if endpoint_name in {'station'}:
        value = app.storage.user\
            .get(page_key)\
            .get(endpoint_name)
        
    selected_value = ui.select(
        data,
        label=label,
        value=value,
        with_input=True
    ).props('outlined dense').classes('w-full')
# s('w-60 bg-gray-200 rounded-md px-3 text-gray-800')
    
    
    async def apply_filters():
        if endpoint_name in {'company'}:
            context = app.storage.user.get('context', {})
            context['company_id'] = selected_value
            app.storage.user['context'] = context

        if endpoint_name in {'station'}:
            staion_id = selected_value.value
            page = app.storage.user.get('pages')
            page_state = page.get(page_key)
            page[page_key] = page_state
            app.storage.user['pages'] = page
            utils.logger.debug(f"page_state: {page_state}")
            
        
        if on_change:
            await on_change()
    
    async def on_select_change(e):
        await apply_filters()
    
    selected_value.on('update:model-value', on_select_change)
    # ui.button('Применить', on_click=apply_filters)