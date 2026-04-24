from core.base_db import Base
from core.logger.logger import make_logger
from datetime import datetime
import json

logger = make_logger(__name__, use_telegram=False)


class RunPiplines:
    def __init__(self, base_db: "Base"):
        self.db = base_db



    async def insert(self, user_id:int, type_method:str, run_mode:str,  
                     operator:str, status: str, last_success_at:datetime,run_id, meta:dict
    ):
        q= """
            INSERT INTO run_pipelines(
            user_id,
            type_method, 
            run_mode,  
            operator, 
            status, 
            last_success_at, 
            run_id, 
            meta
            )
            VALUES (
                $1, $2, $3, $4, $5, $6, $7, $8
            )
            """
        async with self.db.pool.acquire() as conn:
            await conn.execute(
                q,
                user_id,
                type_method,
                run_mode,  
                operator, 
                status, 
                last_success_at, 
                run_id,
                json.dumps(meta, ensure_ascii=False)
            )

