import httpx
import os
from dotenv import load_dotenv
from nicegui import app, ui
from fastapi import Request
from frontend.utils.utils import utils
load_dotenv()


def get_auth_headers(request: Request = None):
    if not request:
        return {}
    data_dict = utils.current_user.get_current_user(request=request)
    token = data_dict['token']
    if not token:
        return {}
    return {
        "Authorization": f"Bearer {token}"
    }


class Endpoints:
    endpoints = {
        'dashboard_stats' :{
            'url': 'dashboard/stats',
            'method': 'post'
        },
        'operators_connect' :{
            'url': 'operators/connect',
            'method': 'post'
        },
        'auth_register' :{
            'url': 'auth/register',
            'method': 'post'
        },
        'company' :{
            'url': 'dashboard/companies',
            'method': 'get'
        },
        'auth_login' :{
            'url': 'auth/login',
            'method': 'post'
        },
    }

    @classmethod
    def get_data_endpoints(cls, endpoint_name):
        data = cls.endpoints.get(endpoint_name)
        if not data:
            raise ValueError(f'Endpoint {endpoint_name} not found')
        return data['url'], data['method'] 


client = httpx.AsyncClient(
    base_url=os.getenv("BACKEND_URL"),
    timeout=10.0,
    # cookies={}
)

async def universal_api(
        endpoint_name: str, 
        payloads: dict = None, 
        params: dict = None,
        request: Request = None,
       
    ):
    
    headers = get_auth_headers(request=request)
    url, method = Endpoints.get_data_endpoints(endpoint_name)
  
    try:
        if method == 'post':
            response = await client.post(
                url=url,
                headers=headers,
                json=payloads,
            )
        elif method == 'get':
            response = await client.get(
                url=url,
                headers=headers,
                params=params,
            )
    except httpx.RequestError as e:
        utils.logger.error(f"{endpoint_name}: {e}")
        return {'error': 'network'}
    try:
        data = response.json()
    except Exception:
        data = None
    
    if response.status_code == 401:
        app.storage.user.clear()
        ui.notify('Сессия истекла', color='red')
        ui.navigate.to('/login')
        return {'error': 'unauthorized'}
    return {
        'status_code': response.status_code,
        'data': data
    }