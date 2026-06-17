from core.base_db import Base


class InvestmentsDB:
    def __init__(self, base_db: "Base"):
        self.db = base_db

    async def insert(
        self, 
        user_id: int,
        station_id: int,
        mode: str,
        amount_type: str,
        amount: float,
        expense_date: str,
        comment: str = None
    ):
        q = """
            INSERT INTO finance_operations (
                user_id,
                station_id,
                mode,
                amount_type,
                amount,
                expense_date,
                comment
            )
            VALUES ($1, $2, $3, $4, $5, $6)
            """
        async with self.db.pool.acquire() as conn:
            await conn.execute(
                q,
                user_id,
                station_id,
                mode,
                amount_type,
                amount,
                expense_date,
                comment
            )