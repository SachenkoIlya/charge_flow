from core.base_db import Base
from datetime import datetime
from asyncpg import Record  

class FinanceDB:
    def __init__(self, base_db: "Base"):
        self.db = base_db
        

    async def get_metrics(
        self, 
        user_id:int, 
        date_to: datetime=None, 
        date_from:datetime=None
    ) -> Record:
        q = """
            SELECT 
                COALESCE(
                    SUM(cs.gross_revenue), 0
                ) AS total_revenue

            FROM  charging_sessions_fact cs
            WHERE user_id = $1
                AND cs.state = 'COMPLETED'
                AND ($2::timestamp IS NULL OR cs.start_ts >= $2)
                AND ($3::timestamp IS NULL OR cs.start_ts < $3)
            """ 
        async with self.db.pool.acquire() as conn:
            return await conn.fetchrow(q, user_id, date_from, date_to)


    async def get_investment(
        self, 
        user_id: int, 
        mode: str,
        date_to: datetime | None=None, 
        date_from: datetime | None=None,
         
    ) -> list[Record]:
        q = """
            SELECT 
                f.id,
                f.amount_type,
                f.amount,
                f.created_at
            FROM finance_operations f
            WHERE user_id = $1
            AND mode = $2
            AND ($3::timestamp IS NULL OR f.created_at >= $3)
            AND ($4::timestamp IS NULL OR f.created_at < $4)
            
            ORDER BY f.id
            """ 
        async with self.db.pool.acquire() as conn:
            return await conn.fetch(q, user_id, mode, date_from, date_to)
