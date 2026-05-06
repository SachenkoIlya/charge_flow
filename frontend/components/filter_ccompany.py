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
        endpoint_name: str=None
    ):
    if not data:
        if not endpoint_name:
            data = selected_company
        else:
            data = await load_data(request=request, endpoint_name=endpoint_name)

    context = app.storage.user.get('context', {})
    selected_company = context.get('company_id')
    
    if selected_company not in data:
        selected_company = None
    
    company_select = ui.select(
        data,
        label=label,
        value=selected_company,
        with_input=True
    ).props('outlined dense').classes('w-full')
# s('w-60 bg-gray-200 rounded-md px-3 text-gray-800')
    
    
    async def apply_filters():
        company_id = company_select.value
        context = app.storage.user.get('context', {})
        context['company_id'] = company_id
        app.storage.user['context'] = context

        if on_change:
            await on_change()
    
    async def on_select_change(e):
        await apply_filters()
    
    company_select.on('update:model-value', on_select_change)
    # ui.button('Применить', on_click=apply_filters)