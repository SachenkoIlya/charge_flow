from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.base_db import Base

from etl.main.users import build_users
from etl.main.context import build_ctx
from etl.main.schemas import RunConfig, RunContextMeta
from etl.main.schemas import RunConfig
from etl.core.run_pipelines import RunPipelines
import aiohttp

from core.logger.logger import logger
from pydantic import ValidationError




async def main(
    type_method: str, 
    run_mode: str, 
    operator: str, 
    base_db: "Base", 
    sessions:aiohttp.ClientSession, 
    user_id: int = None
):
    run = RunPipelines()
    meta = RunContextMeta()

    try:
        config = RunConfig(
            run_mode=run_mode,
            operator=operator,
            type_method=type_method,
            user_id=user_id
        )
    except ValidationError as e:
        logger.error("Ошибка параметров main:", e)
        return {
            'status': 'error',
            'skip': True,
        }
    
    ctx = build_ctx(
        config=config,
        meta=meta,
        base_db=base_db,
        sessions=sessions
    )
    users = await build_users(ctx, meta)
    if not users:
        return {
            'status': 'empty',
            'skip': True
        }
    
    await run._run(
        run_context=users,
        ctx=ctx,
    )
    return {
        'status': 'success',
        'skip': False
    }
    
   
