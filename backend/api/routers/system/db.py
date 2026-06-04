from core.base_db import Base


class SystemDb:
    def __init__(self, base_db: "Base"):
        self.db = base_db


    async def get_data_etl_run(self):
        q = """
            SELECT 
                user_id,
                type_method,
                run_mode,
                operator,
                status,
                last_success_at,
                created_at,
                run_id
              
            FROM run_pipelines
            ORDER BY created_at DESC
            LIMIT 30;
            """
        async with self.db.pool.acquire() as conn:
            return await conn.fetch(q)
        

    async def get_data_bi_exports(self):
        q = """
            SELECT
                user_id,
                type_method,
                run_mode,
                operator,
                status,
                last_success_at,
                created_at,
                run_id,
                error
            FROM bi_exports
            ORDER BY created_at DESC
            LIMIT 30;
            """
        async with self.db.pool.acquire() as conn:
            return await conn.fetch(q)