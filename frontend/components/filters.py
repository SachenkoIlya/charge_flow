from nicegui import ui, app
from frontend.utils.utils import utils
from frontend.api.client import universal_api, frontend_api
from fastapi import Request 


selected_station = {
    '1': 'Все станции',
    '2': 'Станция 1',
    '3': 'Станция 2',
    '4': 'Станция 3'
}
async def load_data(request:Request, endpoint_name:str):
    data = await frontend_api(
        request=request,
        endpoint_name=endpoint_name,
    )
    if data is None:
        return {}
    return {item['id']: item['name'] for item in data}




async def get_filtered_data(
        request: Request, 
        data: dict = None, 
        label:str=None,
        on_change=None,
        endpoint_name: str=None,
        page_key: str=None
    ):
    
    if not data:
        if endpoint_name in {'station'}:
            data = selected_station
        else:
            data = await load_data(
                request=request, 
                endpoint_name=endpoint_name
            )
    
    if endpoint_name in {'company'}:
        value = (
            app.storage.user
            .get('context', {})
            .get(f'{endpoint_name}_id', {})
        )
    if endpoint_name in {'station'}:
        value = (
            app.storage.user
            .get('pages')
            .get(page_key)
            .get(endpoint_name)
        )
    select = ui.select(
        data,
        label=label,
        value=value,
        with_input=True
    ).props('outlined dense').classes('w-full')
    
    
    async def apply_filters():
        if endpoint_name in {'company'}:
            context = app.storage.user.get('context', {})
            context['company_id'] = select.value
            app.storage.user['context'] = context

        if endpoint_name in {'station'}:
            pages = app.storage.user.get('pages')
            page_state = pages.get(page_key)
                
            page_state[endpoint_name] = select.value
            
            pages[page_key] = page_state

            app.storage.user['pages'] = pages
            
        
        if on_change:
            await on_change()
    
    async def on_select_change(e):
        await apply_filters()
    
    select.on('update:model-value', on_select_change)