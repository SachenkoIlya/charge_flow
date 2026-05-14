from etl.utils.config.reports import ReportConfig
from core.base_db import Base

from core.http.aiohttp_client import get_client
from core.logger.logger import logger
from etl.main.main import main
from etl.main.schemas import RunConfig
from pydantic import ValidationError
import asyncio
from core.security.settings import settings


async def run_all_endpoints(run_mode: str, operator: str, delay:int=60):
    try:
        config = RunConfig(
            run_mode=run_mode,
            operator=operator
        )
    except ValidationError as e:
        logger.error("Ошибка конфига запуска:", e)
        return
    
    sessions = get_client()
    base_db = Base()

    await base_db.connect()
    try:
        type_methods =  ReportConfig.TYPE_METHODS.get(operator, [])
        for idx, type_method in enumerate(type_methods):
            
            data = await main(
                type_method=type_method,
                run_mode=config.run_mode,
                operator=config.operator,
                base_db=base_db,
                sessions=sessions,
            )
            status = data.get('status')
            skip = data.get('skip')
            
            logger.debug(f"{type_method} status: {status}")
            if not skip:
                if idx < len(type_methods) - 1:
                    logger.info(f"Пауза {delay} секунд перед следующим типом отчёта")
                    await asyncio.sleep(delay)

    finally:
        await sessions.close()
        await base_db.close()





if __name__ == '__main__':
    # etl\main\runner.py
    # py -m etl.main.runner volt
    import sys

    if len(sys.argv) < 1:
        raise RuntimeError("operator is required")
    operator = sys.argv[1]
    
    asyncio.run(run_all_endpoints(settings.MODE, operator))   
    