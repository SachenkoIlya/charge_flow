from core.http.aiohttp import BaseAiohttpClient
from core.security.settings import settings
from frontend.api.endpoints import Endpoints
from fastapi import Request
from frontend.api.error import handle_frontend_api_error
from frontend.utils.get_token import get_token_from_request
import aiohttp

session: aiohttp.ClientSession | None = None

async def get_session(total:int=10) -> aiohttp.ClientSession:
    """Возвращает или инициализирует глобальную сессию aiohttp.

    Реализует паттерн Singleton для повторного использования одного и того же
    объекта ClientSession между запросами, что оптимизирует пул соединений.

    Args:
        total: Максимальное время ожидания (таймаут) для всех операций 
            в рамках запроса (в секундах). По умолчанию 10.

    Returns:
        aiohttp.ClientSession: Активный экземпляр клиентской сессии.
        
    Note:
        Функция использует глобальную переменную `session`. Если сессия 
        еще не создана или была закрыта, инициализируется новый экземпляр 
        с базовым URL-адресом из настроек (`settings.BACKEND_URL`).
    """
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
    """Выполняет асинхронный запрос к бэкенд-API и возвращает результат.

    Функция выступает в роли прокси-слоя: извлекает токен авторизации из входящего
    запроса, определяет URL и HTTP-метод по имени эндпоинта, выполняет запрос
    через `BaseAiohttpClient` и обрабатывает возможные исключения.

    Args:
        endpoint_name (str, optional): Ключ/имя эндпоинта для получения 
            маршрута и метода из `Endpoints.get_data_endpoints`.
        payloads (dict, optional): Данные тела запроса (body) для HTTP-метода POST.
        params (dict, optional): Параметры строки запроса (query params) для GET.
        request (Request, optional): Объект входящего HTTP-запроса, из которого
            извлекается токен авторизации (например, куки или заголовки).
        auth_type (str): Тип используемой авторизации (например, 'bearer').
            По умолчанию 'bearer'.

    Returns:
        dict | Any | None: Ответ от бэкенд-сервера при успешном запросе.
            Возвращает `None`, если в процессе выполнения произошла ошибка.

    Raises:
        Exception: Внутренние исключения не выбрасываются наружу, а перехватываются
            и обрабатываются функцией `handle_frontend_api_error`.
    """
    
    session = await get_session()
    client = BaseAiohttpClient(session=session)

    token = get_token_from_request(request=request)
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
