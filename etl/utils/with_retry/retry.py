from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from etl.users.users import Users

from core.logger.logger import make_logger
from collections import defaultdict
import asyncio
import random
import aiohttp



logger = make_logger(__name__, use_telegram=False)

# Для каждого токена -> словарь {loop: Lock}
_token_locks = defaultdict(dict)
_last_at = defaultdict(dict)
MIN_GAP = 2.0


def get_lock(token: str) -> asyncio.Lock:
    """
    Возвращает asyncio.Lock для конкретного токена в рамках текущего event loop.

    Используется для сериализации запросов к API для одного клиента
    (например, username или API-токена), чтобы избежать параллельных
    запросов и превышения rate limit.

    Для каждого event loop создаётся отдельный Lock.
    """
    loop = asyncio.get_running_loop()
    if loop not in _token_locks[token]:
        _token_locks[token][loop] = asyncio.Lock()
    return _token_locks[token][loop]



def get_last_at(token: str) -> float:
    """
    Возвращает время последнего запроса для указанного токена
    в рамках текущего event loop.

    Используется для контроля минимального интервала между запросами
    к API (rate limiting).
    """
    loop = asyncio.get_running_loop()
    return _last_at[token].get(loop, 0.0)


def set_last_at(token: str, value: float):
    """
    Сохраняет время последнего выполненного запроса для указанного токена
    в текущем event loop.

    Это значение используется функцией _respect_min_gap для расчёта
    паузы перед следующим запросом.
    """
    loop = asyncio.get_running_loop()
    _last_at[token][loop] = value


async def _respect_min_gap(token: str):
    """
    Гарантирует минимальный интервал (MIN_GAP) между запросами
    к API для конкретного токена.

    Если предыдущий запрос был выполнен слишком недавно,
    функция приостанавливает выполнение через asyncio.sleep,
    чтобы выдержать требуемую паузу и избежать HTTP 429
    (Too Many Requests).

    После ожидания обновляет время последнего запроса.
    """
    now = asyncio.get_running_loop().time()

    wait = get_last_at(token) + MIN_GAP - now
    if wait > 0:
        await asyncio.sleep(wait)

    set_last_at(token, asyncio.get_running_loop().time())


async def with_retry(sessions: aiohttp.ClientSession,  
                     type_method:str, method:str, user: "Users",
                     body:dict = None, url=None, tries=8
    ):
   
    backoff = 1.0
    for attempt in range(1, tries + 1):
        
        async with get_lock(user.login):
            await _respect_min_gap(user.login)
      
            try:
                if method == "get":
                    async with sessions.get(
                        url=url,
                        auth=aiohttp.BasicAuth(
                            user.login, 
                            user.password,
                        ),
                        params=body
                    ) as response:
                        logger.debug(response.request_info.real_url)
                        if response.status == 200:
                            return await response.json()

                        if response.status == 204:
                            return []

                        if response.status == 429:
                            res = response.headers.get("Retry-After")
                            try:
                                wait = float(res) if res else backoff + \
                                    random.uniform(0, backoff / 2)
                            except Exception:
                                wait = backoff + random.uniform(0, backoff / 2)
                            logger.warning(
                                f"[{user.id}][{type_method}] 429 → жду {wait:.1f} сек (попытка {attempt}/{tries})"
                            )

                            await asyncio.sleep(wait)
                            backoff = min(backoff * 2, 60)
                            continue
                        
                        if response.status in (401, 403, 404, 500):
                            raise RuntimeError(await response.text())
                        text = await response.text()

                        raise RuntimeError(f"HTTP {response.status}: {text}")
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, 60)
                continue

    raise RuntimeError(f" Max retries exceeded")
