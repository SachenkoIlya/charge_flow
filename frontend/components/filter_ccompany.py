from nicegui import ui, app
from frontend.utils.utils import utils
from frontend.api.client import universal_api
from fastapi import Request 
import asyncio 



async def fetch_companies(request:Request, endpoint_name ='dashboard_companies'):
    
    data = await universal_api(
        endpoint_name=endpoint_name,
        request=request,

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

    return {item['id']: item['name'] for item in answer}




async def get_filtered_company_from_admin(
        request: Request, 
        companies: dict = None, 
        on_change=None
    ):
    if not companies:
        companies = await fetch_companies(request=request)

    filters = app.storage.user.get('filters', {})
    selected_company = filters.get('company_id')
    
    if selected_company not in companies:
        selected_company = None
    
    company_select = ui.select(
        companies,
        label='Компания',
        value=selected_company,
        with_input=True
    ).props('dense borderless clearable label-color=primary')\
    .classes('w-60 bg-gray-200 rounded-md px-3 text-gray-800')
    
    
    async def apply_filters():
        company_id = company_select.value
        filters = app.storage.user.get('filters', {})
        filters['company_id'] = company_id
        app.storage.user['filters'] = filters

        if on_change:
            await on_change()
    
    async def on_select_change(e):
        await apply_filters()
    
    company_select.on('update:model-value', on_select_change)
    # ui.button('Применить', on_click=apply_filters)