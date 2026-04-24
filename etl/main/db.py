
from core.base_db import Base
from core.logger.logger import make_logger
from zoneinfo import ZoneInfo

logger = make_logger(__name__, use_telegram=False)


class RunRepository:
    def __init__(self, base_db: "Base"):
        self.db = base_db

    @Base.with_retries(retries=5, delay=1.5, msg_prefix='RunRepository.get_single_users')
    async def get_schema_preview(self, limit: int = 1):
        q = f"""
            SELECT * FROM operator_credentials
            LIMIT $1
            """
        async with self.db.pool.acquire() as conn:
            return (
                await conn.fetchrow(q, limit)
                if limit == 1
                else await conn.fetch(q, limit)
            )
                   
        

    @Base.with_retries(retries=5, delay=1.5, msg_prefix='RunRepository.get_single_users')
    async def get_single_users(self, user_id: int):
        q_single = """
            SELECT * FROM operator_credentials
            WHERE user_id = $1
        """
        async with self.db.pool.acquire() as conn:
            return await conn.fetchrow(q_single, user_id) 

    @Base.with_retries(retries=5, delay=1.5, msg_prefix='RunRepository.get_users')
    async def get_users(self):
        q = """
                SELECT * FROM operator_credentials
            """
        async with self.db.pool.acquire() as conn:
            return await conn.fetch(q)
            




    @Base.with_retries(retries=5, delay=1.5, msg_prefix='RunRepository.get_last_success')
    async def get_last_success(self, user_id: int, type_method: str, run_mode: str, operator: str):
        q = """
            SELECT last_success_at from run_pipelines
            WHERE user_id = $1
                AND type_method = $2
                AND run_mode = $3
                AND operator = $4
                AND status = 'success'
            ORDER BY created_at DESC
            LIMIT 1;
        """
        async with self.db.pool.acquire() as conn:
            row = await conn.fetchrow(
                q,
                user_id,
                type_method,
                run_mode,
                operator
            )
        
        if not row:
            logger.warning(
                f"🆕 Первый запуск для store_id={user_id}, "
                f"operator={operator}, type_method={type_method} — успешных run не найдено"
            )
            return None
        
        logger.info(
            f"🔎 Последний успешный run найден: "
            f"{row['last_success_at']} (UTC)"
        )

        last_time_zone = row['last_success_at'].astimezone(ZoneInfo("Europe/Moscow"))
        return last_time_zone 
        
