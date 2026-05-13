
from core.http.services.auth_type import AuthType
from core.http.services.exception import (
    APIError,
    ClientError,
    UnauthorizedError,
    ForbiddenError,
    NotFoundError,
    ValidationError,
    ConflictError,
    ServerError,
    ServiceUnavailableError,
    NetworkError,
    RetryExceededError,
)
from core.http.rate_limiter import (get_lock, respect_min_gap)
from core.logger.logger import make_logger
import random
import aiohttp
import asyncio 


logger = make_logger(__name__, use_telegram=False)

async def wait_for_retry(resp: aiohttp.ClientResponse, attempt:int, tries:int, backoff:int):
    res = resp.headers.get("Retry-After")
    try:
        wait = float(res) if res else backoff + \
            random.uniform(0, backoff / 2)
    except Exception:
        wait = backoff + random.uniform(0, backoff / 2)
    logger.warning(
        f"429 → жду {wait:.1f} сек (попытка {attempt}/{tries})"
    )
    
    await asyncio.sleep(wait)
    return min(backoff * 2, 60)
     

async def error_handling(resp: aiohttp.ClientResponse, attempt:int, tries:int, backoff:int):
    if resp.status == 200:
        if resp.content_type == 'application/json':
            return {
                'status': resp.status,
                'data': await resp.json(),
                'backoff': None,
                'retry': False,
            }
        return {
            'status': resp.status,
            'data': await resp.text(),
            'backoff': backoff,
            'retry': False,
        }
    if resp.status == 204:
        return {
                'status': resp.status,
                'data': [],
                'backoff': None,
                'retry': False,
            }
    if resp.status == 429:
        new_backoff = await wait_for_retry(
            resp=resp,
            attempt=attempt,
            tries=tries,
            backoff=backoff
        )
        return {
            'status': resp.status,
            'data': None,
            'backoff': new_backoff,
            'retry': True,
        }
    
    text = await resp.text()
    if resp.status == 401:
        raise UnauthorizedError(text)
    if resp.status == 403:
        raise ForbiddenError(text)
    if resp.status == 404:
        raise NotFoundError(text)
    if resp.status >= 500:
        raise ServerError(text)

class MethodEnum:
    GET:str = 'get'
    POST:str = 'post'


class BaseAiohttpClient:
    def __init__(self,  session: aiohttp.ClientSession):
        self.method_enum = MethodEnum()
        self.session = session
    
    
    
    @staticmethod
    async def with_retry(
        request_method : aiohttp.ClientSession, 
        url: str, 
        headers: dict, 
        params:dict=None,
        auth=None, 
        json:dict=None, 
        tries:int=8, 
        **kwargs
    ):  
        backoff = 1
       
        for attempt in range(1, tries + 1):
            try:
                async with request_method(
                    url=url,
                    params=params,
                    json=json,
                    auth=auth,
                    headers=headers,
                    **kwargs
                ) as response:
                    resp: aiohttp.ClientResponse = response
                    result = await error_handling(
                        resp=resp,
                        attempt=attempt,
                        tries=tries,
                        backoff=backoff
                    )
                    backoff = result['backoff']
                    if result['retry']:
                        continue
                    return result['data']
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, 60)
                continue
        raise RetryExceededError(f'Max retries exceeded: {url}')
    
    
    async def _requests(
            self, 
            http_method: str, 
            url:str, 
            auth_type:str,
            login: str=None,
            password:str=None,
            api_key:str=None,
            params: dict=None,
            json:dict=None, 
            use_rate_limit: bool = None,
            **kwargs
    ):
        """
        
        """

        auth = AuthType(
            auth_type=auth_type,
            login=login,
            password=password,
            api_key=api_key
        )
        aiohttp_data = auth.get_auth_headers()
        token = aiohttp_data.get('token')
        headers = aiohttp_data.get('headers')
        aiohttp_auth = aiohttp_data.get('aiohttp_auth')
       
        request_method : aiohttp.ClientSession = getattr(self.session, http_method)
        
        if use_rate_limit:
            async with get_lock(token):
                await respect_min_gap(token)
                return await self.with_retry(
                    request_method,
                    url,
                    headers=headers,
                    auth=aiohttp_auth,
                    params=params,
                    json=json,
                    **kwargs
                )
        else:
            return await self.with_retry(
                request_method,
                url,
                headers=headers,
                auth=aiohttp_auth,
                params=params,
                json=json,
                **kwargs
            )
        
    async def get(
        self, 
        auth_type: str, 
        url:str, 
        payload: dict, 
        login:str=None, 
        password:str=None, 
        api_key:str=None, 
        use_rate_limit: bool = None,
        **kwargs
    ):
        """Формирует get запрос"""
        return await self._requests(
            self.method_enum.GET, 
            url, 
            auth_type, 
            params=payload,
            login=login,
            password=password,
            api_key=api_key, 
            use_rate_limit=use_rate_limit,
            **kwargs
        )
    
    async def post(
        self, 
        auth_type: str, 
        url:str, 
        payload: dict, 
        login:str=None, 
        password:str=None, 
        api_key:str=None, 
        use_rate_limit: bool = None,
        **kwargs
    ):
        """Формирует post запрос"""
        return await self._requests(
            self.method_enum.POST,
            url,
            auth_type,
            json=payload,
            login=login,
            password=password,
            api_key=api_key,
             use_rate_limit=use_rate_limit,
            **kwargs
        )
    
