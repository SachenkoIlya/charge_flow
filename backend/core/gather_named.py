from core.logger.logger import logger
import asyncio



async def gather_named(tasks: dict):
    result = await asyncio.gather(*tasks.values(), return_exceptions=True)
    data = {}
    for name, res in zip(tasks.keys(), result):
        if isinstance(res, Exception):
            logger.error(f"{name}: {str(res)}")
            data[name] = None
        else:
            data[name] = res
    return data