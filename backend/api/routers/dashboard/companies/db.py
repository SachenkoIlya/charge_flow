from core.base_db import Base

class UserRepositoryDB:
    def __init__(self, base_db: "Base"):
        self.db = base_db

    
    async def get_company(self):
        q = """
            SELECT 
                id, company 
            FROM users_new
            WHERE role = 'investor'
            """
        async with self.db.pool.acquire() as conn:
            return await conn.fetch(q)