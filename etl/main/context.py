from etl.main.schemas import RunConfig, RunContextMeta
from etl.utils.context.ctx import Ctx
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.base_db import Base
import aiohttp


def build_ctx(config: RunConfig,
    meta: RunContextMeta,
    base_db: "Base",
    sessions: aiohttp.ClientSession,
) -> "Ctx":
    return Ctx(
        type_method=config.type_method,
        base_db=base_db,
        session=sessions,
        run_mode=config.run_mode,
        run_id=meta.run_id,
        operator=config.operator
        )