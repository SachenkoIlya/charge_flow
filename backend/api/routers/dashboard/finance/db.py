from core.base_db import Base
from datetime import datetime
from asyncpg import Record  

class FinanceDB:
    def __init__(self, base_db: "Base"):
        self.db = base_db
        

    async def get_metrics(
        self, 
        user_id:int, 
        date_from:datetime=None,
        date_to: datetime=None, 
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
        async with self.db.get_conn() as conn:
            return await conn.fetchrow(
                q, 
                user_id, 
                date_from, 
                date_to
            )

    async def get_date_range(self, user_id:int):
        q = """
            SELECT
                MIN(cs.start_ts) as first_date,
                MAX(cs.start_ts) as  last_date
            FROM charging_sessions_fact cs
            WHERE user_id = $1
            AND cs.state = 'COMPLETED';
            """
        async with self.db.get_conn() as conn:
            return await conn.fetchrow(q, user_id)
    async def get_investment(
        self, 
        user_id: int, 
        mode: str,
        date_from: datetime | None=None,
        date_to: datetime | None=None
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
        async with self.db.get_conn() as conn:
            return await conn.fetch(
                q, 
                user_id, 
                mode, 
                date_from, 
                date_to
            )

    async def get_investment_group(
        self,
        user_id: int,
        date_from: datetime | None=None,
        date_to: datetime | None=None,
    ) ->list[Record]:
        q = """
            SELECT
                f.mode
                , f.amount_type
                , COALESCE(
                    SUM(f.amount)
                    , 0
                ) AS amount

            FROM finance_operations f
            WHERE user_id = $1
                AND ($2::timestamp IS NULL or f.expense_date >= $2)
                AND ($3::timestamp IS NULL or f.expense_date < $3)
            GROUP BY 
                f.mode, f.amount_type
            """
        async with self.db.get_conn() as conn:
            return await conn.fetch(q, user_id, date_from, date_to)
        
    async def get_investment(
        self, 
        user_id: int, 
        date_from: datetime | None=None,
        date_to: datetime | None=None, 
    ) -> list[Record]:
        q = """
            SELECT 
                f.mode,
                COUNT(*) as operations_count,
                COALESCE(
                    SUM(f.amount),
                    0
                ) as total_amount
            FROM finance_operations f
            WHERE user_id = $1
                AND ($2::timestamp IS NULL or f.expense_date >= $2)
                AND ($3::timestamp IS NULL or f.expense_date < $3)
            GROUP BY f.mode
            """
        async with self.db.get_conn() as conn:
            return await conn.fetch(
                q,
                user_id,
                date_from,
                date_to
            )
        
    async def get_network_cost_structure(
        self, 
        user_id: int, 
        date_from: datetime | None=None,
        date_to: datetime | None=None, 
        mode:str = 'opex'
    ) -> list[Record]:
        q = """
            SELECT 
                COALESCE(
                    SUM(f.amount) FILTER(
                        WHERE f.amount_type = 'electricity_compensation'
                    )
                    , 0
                ) as electricity_compensation
                ,
                COALESCE(
                    SUM(f.amount) FILTER(
                        WHERE f.amount_type = 'rent_payment'
                    )
                    , 0
                ) as rent_payment
                ,
                COALESCE(
                    SUM(f.amount) FILTER(
                        WHERE f.amount_type = 'operator_commission'
                    )
                    , 0
                ) as operator_commission
                ,
                COALESCE(
                    SUM(f.amount) FILTER(
                        WHERE f.amount_type = 'service_maintenance'
                    )
                    , 0
                ) as service_maintenance
                ,
                COALESCE(
                    SUM(f.amount) FILTER(
                        WHERE f.amount_type = 'internet_and_connection'
                    )
                    , 0
                ) as internet_and_connection
                ,
                COALESCE(
                    SUM(f.amount) FILTER(
                        WHERE f.amount_type = 'taxes'
                    )
                    , 0
                ) as taxes

            FROM finance_operations f

            WHERE user_id = $1
                AND ($2::timestamp IS NULL or f.expense_date >= $2)
                AND ($3::timestamp IS NULL or f.expense_date < $3)
                AND mode = $4
            """
        async with self.db.get_conn() as conn:
            return await conn.fetch(
                q,
                user_id,
                date_from,
                date_to,
                mode
            )
        

      
     