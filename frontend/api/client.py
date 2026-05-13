from core.http.aiohttp import BaseAiohttpClient
from core.http.aiohttp_client import get_client
from core.security import settings
from frontend.api.endpoints import Endpoints

from fastapi import Request
from frontend.api.error import handle_frontend_api_error
from frontend.utils.utils import utils
import   aiohttp

def get_token_from_request(request: Request = None):
    if not request:
        return {}
    data_dict = utils.current_user.get_current_user(request=request)
    token = data_dict['token']
    if not token:
        return None
    return token



  
frontend_session = aiohttp.ClientSession(
    base_url=settings.BACKEND_URL,
    timeout=10.0
)
async def frontend_api(
        endpoint_name=None,
        payloads=None,
        params: dict = None,
        request: Request = None,
        auth_type: str = 'bearer',
):
   
    client = BaseAiohttpClient(frontend_session)

    token = get_token_from_request(request=request)
    url, method = Endpoints.get_data_endpoints(endpoint_name)
    try:
        if method == 'post':
            response = await client.post(
                auth_type=auth_type,
                url=url,
                api_key=token,
                payload=payloads or {},
            )
        else:
            response = await client.get(
                auth_type=auth_type,
                url=url,
                api_key=token,
                payload=params or {},
            )
    except Exception as e:
        await handle_frontend_api_error(e)
        return None
    return response
