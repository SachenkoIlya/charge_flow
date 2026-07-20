from core.base_db import Base


class InvestmentsDB:
    """Низкоуровневый интерфейс базы данных для финансовых операций.
    
    Выполняет прямые SQL-запросы к таблице `finance_operations`.
    """
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
        """Записывает одну финансовую операцию (категорию расхода) в базу данных.

        Args:
            user_id: Идентификатор пользователя, создавшего запись.
            station_id: Идентификатор станции, к которой привязан расход.
            mode: Тип финансовых затрат ('capex' или 'opex').
            amount_type: Конкретная категория расхода (например, 'rent_payment').
            amount: Денежная сумма операции.
            expense_date: Дата совершения расхода.
            comment: Необязательный текстовый комментарий. По умолчанию None.

        Returns:
            None
        """
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
            VALUES ($1, $2, $3, $4, $5, $6, $7)
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
    
    @Base.with_retries(retries=5, delay=1.5, msg_prefix='update_bi_exports')
    async def execute_many_query(self, records:list[tuple]):
        q = """
                INSERT INTO finance_operations(
                    user_id, station_id, expense_date, comment, mode, amount_type, amount
                )
                VALUES(
                    $1, $2, $3, $4, $5, $6, $7
                )
            """
        async with self.db.pool.acquire() as conn:
            await conn.executemany(q, records)

        