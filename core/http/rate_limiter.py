from collections import defaultdict
import base64
import asyncio
from core.logger.logger import make_logger


logger = make_logger(__name__, use_telegram=False)

MIN_GAP = 2.0
_token_locks: dict[str, asyncio.Lock] = {}
_last_at: defaultdict[str, float] = defaultdict(float)

def get_lock(token: str)-> asyncio.Lock:
    if token not in _token_locks:
        logger.debug(f"[LOCK CREATE] token={token}")
        _token_locks[token] = asyncio.Lock()
    return _token_locks[token]

async def respect_min_gap(token: str):
    loop = asyncio.get_running_loop()
    now = loop.time()
    
    last = _last_at[token]
    wait = last + MIN_GAP - now
    
    logger.debug(
        f"[GAP CHECK] token={token} "
        f"last={last:.3f} now={now:.3f} wait={wait:.3f}"
    )
    if wait > 0:
        logger.debug(f"[WAIT] token={token} sleeping {wait:.2f}s")
        await asyncio.sleep(wait)
    
    new_time = loop.time()
    _last_at[token] = new_time
    logger.debug(f"[SET LAST] token={token} new_time={new_time:.3f}")

