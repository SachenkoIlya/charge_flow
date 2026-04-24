from core.base_db import Base

class ConnectOperator:
    def __init__(self, base_db: "Base"):
        self.db = base_db



    @Base.with_retries(retries=3, delay=1.5, msg_prefix='[ConnectOperator.check_user_existence]')
    async def check_user_existence(self, email: str):
        q = """
            select id, company from users_new
            WHERE email = $1 
            """
        async with self.db.pool.acquire() as conn:
            return await conn.fetchrow(q, email)
        
        
    @Base.with_retries(retries=3, delay=1.5, msg_prefix='[ConnectOperator.check_first_run]')
    async def check_first_run(self, user_id: str, run_mode: str, login: str):
        q = """
            SELECT status FROM run_pipelines
            WHERE user_id = $1
                AND run_mode = $2
                AND login = $3
            """
        async with self.db.pool.acquire() as conn:
            return await conn.fetchrow(
               q,
               user_id,
               run_mode,
               login
            )
        


    @Base.with_retries(retries=3, delay=1.5, msg_prefix='[ConnectOperator.upsert_user_api_keys]')
    async def upsert_user_api_keys(self, user_id: int, auth_type: str, login: str, password: str, operator: str):
        q = """
        INSERT INTO operator_credentials (
            user_id, auth_type, login, password, operator
        )
        VALUES ($1, $2, $3, $4, $5)
        ON CONFLICT (user_id) 
        DO UPDATE 
            SET auth_type = EXCLUDED.auth_type,
                login = EXCLUDED.login,
                password = EXCLUDED.password,
                operator = EXCLUDED.operator
            ;
        """
        async with self.db.pool.acquire() as conn:
            await conn.execute(
               q,
               user_id, 
               auth_type, 
               login, 
               password, 
               operator
            )