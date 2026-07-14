from core.http.aiohttp import BaseAiohttpClient
from core.security.settings import settings
from frontend.api.endpoints import Endpoints
from core.logger.logger import logger   
from fastapi import Request
from frontend.api.error import handle_frontend_api_error
from frontend.utils.utils import utils
import aiohttp

def get_token_from_request(request: Request = None):
    if not request:
        return {}
    data_dict = utils.current_user.get_current_user(request=request)
    token = data_dict['token']
    if not token:
        return None
    return token


session: aiohttp.ClientSession | None = None

async def get_session(total:int=10) -> aiohttp.ClientSession:
    timeout = aiohttp.ClientTimeout(total=total)
    global session 
    if session is None or session.closed:
        session = aiohttp.ClientSession(
            base_url=settings.BACKEND_URL,
            timeout=timeout
        )
    return session

  


async def frontend_api(
        endpoint_name=None,
        payloads=None,
        params: dict = None,
        request: Request = None,
        auth_type: str = 'bearer',
):
    session = await get_session()
    client = BaseAiohttpClient(session=session)

    token = get_token_from_request(request=request)
    logger.debug(f"token: {token}")
    url, method = Endpoints.get_data_endpoints(endpoint_name)
    try:
        if method == 'post':
            response = await client.post(
                auth_type=auth_type,
                url=url,
                api_key=token,
                payload=payloads or {},
                use_rate_limit=False
            )
        else:
            response = await client.get(
                auth_type=auth_type,
                url=url,
                api_key=token,
                payload=params or {},
                use_rate_limit=False
            )
    except Exception as e:
        await handle_frontend_api_error(e)
        return None
    return response
