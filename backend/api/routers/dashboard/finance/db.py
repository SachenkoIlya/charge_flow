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
        station_ids: list[int]=None 
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
                AND (
                    cardinality($4::int[]) = 0
                    OR cs.station_id = ANY($4::int[])
                )
            """ 
        async with self.db.get_conn() as conn:
            return await conn.fetchrow(
                q, 
                user_id, 
                date_from, 
                date_to,
                station_ids 
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


    async def get_investment_group(
        self,
        user_id: int,
        date_from: datetime | None=None,
        date_to: datetime | None=None,
        station_ids: list[int]=None
    ) ->list[Record]:
        q = """
            WITH finance_agg AS (
                SELECT
                    f.mode
                    , f.amount_type
                    , COALESCE(
                        SUM(f.amount)
                        , 0
                    ) AS amount

                FROM finance_operations f
                WHERE user_id = $1
                AND (
                    (
                        f.mode = 'capex'
                        AND (
                            $3::timestamp IS NULL
                            OR f.expense_date < $3
                        )
                    )
                    OR
                    (
                        f.mode = 'opex'
                        AND (
                            $2::timestamp IS NULL
                            OR f.expense_date >= $2
                        )
                        AND (
                            $3::timestamp IS NULL
                            OR f.expense_date < $3
                        )
                    )
                )
                AND (
                    cardinality($4::int[]) = 0
                    OR f.station_id = ANY($4::int[])
                )

                GROUP BY 
                    f.mode, f.amount_type
            ),
            commission_agg AS (
                SELECT
                    COALESCE(SUM(cs.gross_revenue - cs.partner_revenue), 0) as operator_commission
                            
                FROM charging_sessions_fact cs
                            
                WHERE cs.user_id = $1
                    AND ($2::timestamp IS NULL OR cs.start_ts >= $2)
                    AND ($3::timestamp IS NULL OR cs.start_ts < $3)
                    AND  (
                        cardinality($4::int[]) = 0
                        OR cs.station_id = ANY($4::int[])
                    )
            )
            SELECT 
                fa.mode,
                fa.amount_type,
                fa.amount
            FROM finance_agg fa

            UNION ALL

            SELECT 
                'opex' AS mode,
                'operator_commission' AS amount_type,
                ca.operator_commission AS amount
            FROM commission_agg ca

            ORDER BY 
                mode,
                amount_type

            """
        async with self.db.get_conn() as conn:
            return await conn.fetch(
                q, 
                user_id, 
                date_from, 
                date_to,
                station_ids
            )
        
   
        
    async def get_network_cost_structure(
        self, 
        user_id: int, 
        date_from: datetime | None=None,
        date_to: datetime | None=None, 
        station_ids: list[int]=None,
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
                AND  (
                    cardinality($5::int[]) = 0
                    OR f.station_id = ANY($5::int[])
                )
            """
        async with self.db.get_conn() as conn:
            return await conn.fetch(
                q,
                user_id,
                date_from,
                date_to,
                mode,
                station_ids
            )

    async def get_operator_commission(
        self, 
        user_id:int, 
        date_from:datetime=None, 
        date_to:datetime=None,
        station_ids:list[int]=None
    ) ->Record:
        q = """
            SELECT
                COALESCE( 
                    COALESCE(
                        SUM(cs.gross_revenue) 
                        , 0
                    ) 
                    - 
                    COALESCE(
                        SUM(cs.partner_revenue) 
                        , 0
                    ) 
                    ,
                    0
                ) as operator_commission
            FROM charging_sessions_fact cs
            WHERE
                cs.user_id = $1
                AND ($2::timestamp IS NULL or cs.start_ts >= $2)
                AND ($3::timestamp IS NULL or cs.start_ts < $3)
                AND  (
                    cardinality($5::int[]) = 0
                    OR f.station_id = ANY($5::int[])
                )
            """
        async with self.db.get_conn() as conn:
            return await conn.fetchrow(
                q,
                user_id,
                date_from,
                date_to,
                station_ids
            )

    async def get_full_network_cost_structure(
        self,
        user_id: int,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        station_ids:list[int]=None,
        mode: str = 'opex'
        ) -> Record:    
        q = """
            WITH finance_agg AS (
                SELECT
                    COALESCE(SUM(f.amount) FILTER (WHERE f.amount_type = 'electricity_compensation'), 0) as electricity_compensation
                    ,
                    COALESCE(SUM(f.amount) FILTER (WHERE f.amount_type = 'rent_payment'), 0) as rent_payment
                    ,
                    COALESCE(SUM(f.amount) FILTER (WHERE f.amount_type = 'service_maintenance'), 0) as service_maintenance
                    ,
                    COALESCE(SUM(f.amount) FILTER (WHERE f.amount_type = 'internet_and_connection'), 0) as internet_and_connection
                    ,
                    COALESCE(SUM(f.amount) FILTER (WHERE f.amount_type = 'taxes'), 0) as taxes

                FROM finance_operations f
                
                WHERE f.user_id = $1
                    AND ($2::timestamp IS NULL or f.expense_date >= $2)
                    AND ($3::timestamp IS NULL or f.expense_date < $3)
                    AND mode = $4
                    AND  (
                        cardinality($5::int[]) = 0
                        OR f.station_id = ANY($5::int[])
                    )
            ),
            commission_agg AS (
                SELECT
                    COALESCE(SUM(cs.gross_revenue - cs.partner_revenue), 0) as operator_commission
                
                FROM charging_sessions_fact cs
                
                WHERE cs.user_id = $1
                    AND ($2::timestamp IS NULL OR cs.start_ts >= $2)
                    AND ($3::timestamp IS NULL OR cs.start_ts < $3)
                    AND  (
                        cardinality($5::int[]) = 0
                        OR cs.station_id = ANY($5::int[])
                    )
            )
            SELECT
                f_agg.electricity_compensation,
                f_agg.rent_payment,
                f_agg.service_maintenance,
                f_agg.internet_and_connection,
                f_agg.taxes,
                c_agg.operator_commission
            
            FROM finance_agg f_agg
            CROSS JOIN commission_agg c_agg;
        """
        async with self.db.get_conn() as conn:
            return await conn.fetchrow(
                q,
                user_id,
                date_from,
                date_to,
                mode,
                station_ids
            )


    async def get_group_month_cost_structure(
        self,
        user_id: int,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        mode: str = 'opex'
    ) -> list[Record]:
        q = """
            SELECT
                DATE_TRUNC('month', f.expense_date)::date AS month_date
                ,
                COALESCE(
                    SUM(f.amount), 0
                ) as opex_expenses

            FROM finance_operations f
            WHERE f.user_id = $1
                AND mode = $2
               
            GROUP BY month_date
            ORDER BY month_date ASC;
            """
        async with self.db.get_conn() as conn:
            return await conn.fetch(
                q,
                user_id,
                mode,
                # date_from,
                # date_to
            )
        # AND ($3::timestamp IS NULL or f.expense_date >= $3)
        # AND ($4::timestamp IS NULL or f.expense_date < $4)

    async def get_group_month_revenue(self, user_id: int) -> list[Record]:
        q = """
            SELECT
                DATE_TRUNC('month', cs.start_ts)::date AS month_date
                ,
                COALESCE(SUM(cs.gross_revenue), 0) as total_revenue
                ,
                COALESCE(SUM(cs.partner_revenue), 0) as owner_revenue
                ,
                COALESCE(SUM(cs.gross_revenue - cs.partner_revenue), 0) as operator_commission
            FROM charging_sessions_fact cs
            WHERE cs.user_id = $1
            GROUP BY month_date
            ORDER BY  month_date ASC
            """
        async with self.db.get_conn() as conn:
            return await conn.fetch(q, user_id)

    async def get_station_financials(
        self, 
        user_id: int,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        mode: str = 'opex'
    ) -> list[Record]:
        q = """
            WITH sessions_agg AS (
                SELECT
                    cs.station_id
                    ,
                    st.location_name
                    ,
                    COALESCE(SUM(cs.gross_revenue), 0 ) AS total_revenue
                    ,
                    COALESCE(SUM(cs.partner_revenue), 0) as owner_revenue
                    ,
                    COALESCE(SUM(cs.gross_revenue - cs.partner_revenue), 0) as operator_commission
                    
                FROM charging_sessions_fact cs
                    LEFT JOIN info_station st
                    ON st.id = cs.station_id
                    AND st.user_id = cs.user_id
                
                WHERE cs.user_id = $1
                    AND ($2::timestamp IS NULL OR cs.start_ts >= $2)
                    AND ($3::timestamp IS NULL OR cs.start_ts < $3)
                
                GROUP BY cs.station_id, st.location_name
            ),
            finance_agg AS (
                SELECT
                    f.station_id
                    ,
                    COALESCE(SUM(f.amount) FILTER (WHERE f.amount_type = 'electricity_compensation'), 0) as electricity_compensation
                    ,
                    COALESCE(SUM(f.amount) FILTER (WHERE f.amount_type = 'rent_payment'), 0) as rent_payment
                    ,
                    COALESCE(SUM(f.amount) FILTER (WHERE f.amount_type = 'service_maintenance'), 0) as service_maintenance
                    ,
                    COALESCE(SUM(f.amount) FILTER (WHERE f.amount_type = 'internet_and_connection'), 0) as internet_and_connection
                    ,
                    COALESCE(SUM(f.amount) FILTER (WHERE f.amount_type = 'taxes'), 0) as taxes
                    ,
                    COALESCE(SUM(f.amount) FILTER (WHERE f.amount_type = 'insurance'), 0) as insurance
                    ,
                    COALESCE(SUM(f.amount) FILTER (WHERE f.amount_type = 'other_expenses'), 0) as other_expenses
                FROM finance_operations f
                
                WHERE f.user_id = $1 
                    AND ($2::timestamp IS NULL or f.expense_date >= $2)
                    AND ($3::timestamp IS NULL or f.expense_date < $3)
                    AND f.mode = $4
                
                GROUP BY station_id
            )
       
            SELECT
                s.station_id,
                s.location_name,

                s.total_revenue,
                s.owner_revenue,
                s.operator_commission,

                COALESCE(f.electricity_compensation, 0)
                    AS electricity_compensation,
                COALESCE(f.rent_payment, 0)
                    AS rent_payment,
                COALESCE(f.service_maintenance, 0)
                    AS service_maintenance,
                COALESCE(f.internet_and_connection, 0)
                    AS internet_and_connection,
                COALESCE(f.insurance, 0)
                    AS insurance,
                COALESCE(f.other_expenses, 0)
                    AS other_expenses,
                COALESCE(f.taxes, 0)
                    AS taxes

            FROM sessions_agg s
            LEFT JOIN finance_agg f
                ON f.station_id = s.station_id
            ORDER BY s.total_revenue DESC;
            """
        async with self.db.get_conn() as conn:
            return await conn.fetch(
                q,
                user_id, 
                date_from, 
                date_to, 
                mode
            )