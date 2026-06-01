from core.logger.logger import logger

async def submit(data:dict):
    logger.debug(f"зашли в submit")
    logger.debug(data)