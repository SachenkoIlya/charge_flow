from core.base_db import Base
from datetime import datetime
from asyncpg import Record


class ChartsDB:
    def __init__(self, base_db: "Base"):
        self.db = base_db

    
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
        async with self.db.pool.acquire() as conn:
            return await conn.fetch(
                q,
                user_id,
                date_from,
                date_to,
                mode
            )
        
    
    async def get_metrics_time_series(
        self, 
        user_id: int, 
        date_from: datetime, 
        date_to: datetime, 
        date_expr: str
    ) -> list[Record]:
        """
        Получает агрегированные данные для построения графиков за указанный период.

        Метод группирует зарядные сессии по переданному временному выражению
        (`date_expr`) и возвращает показатели по каждому периоду.

        Args:
            user_id (int): Идентификатор пользователя.
            date_from (datetime): Начало периода выборки (включительно).
            date_to (datetime): Конец периода выборки (не включительно).
            date_expr (str): SQL-выражение для группировки по периоду,
                например день, неделя или месяц.

        Returns:
            list[asyncpg.Record]:
                Список записей с агрегированными данными по периодам:

                - period — период группировки;
                - evse_count (int) — общее количество уникальных EVSE;
                - sessions (int) — количество зарядных сессий за период;
                - revenue (numeric) — выручка по завершённым сессиям;
                - charging_minutes (numeric) — длительность завершённых зарядок в минутах.

        Notes:
            - Метод использует `fetch()`, поэтому возвращает список записей.
            - Если данных за период нет, вернётся пустой список.
            - В расчёт `revenue` и `charging_minutes` включаются только
            сессии со статусом `COMPLETED`.
        """
        q = f"""
            WITH evse_total AS (
                SELECT
                    COUNT(DISTINCT cs.evse_path) AS evse_count
                FROM charging_sessions_fact cs
                WHERE cs.user_id = $1
            )
            SELECT
                {date_expr} as period
                ,
                (SELECT evse_count FROM evse_total) AS evse_count
                ,
                COUNT(*) AS sessions
                ,
                COALESCE(
                    SUM(cs.gross_revenue)
                        FILTER(WHERE cs.state = 'COMPLETED'),
                        0
                ) AS revenue
                ,
                COALESCE(
                    SUM(cs.charge_duration_minutes)
                        FILTER(WHERE cs.state = 'COMPLETED'),
                        0
                ) AS charging_minutes
            FROM charging_sessions_fact cs
            WHERE user_id = $1
                AND cs.start_ts >= $2
                AND cs.start_ts < $3 
            GROUP BY period
            ORDER BY period
            """
        async with self.db.pool.acquire() as conn:
            return await conn.fetch(q, user_id, date_from, date_to)