from core.base_db import Base
from asyncpg import Record
from datetime import datetime


class TableDB:
    def __init__(self, base_db: "Base"):
        self.db = base_db
    
    async def get_station_revenue_stats(
        self, 
        user_id:int, 
        date_from:datetime, 
        date_to:datetime
    ) -> list[Record]:
        q = """
            SELECT 
                cs.station_id
                ,
                MAX(s.location_name) AS station_name
                ,
                COALESCE(
                    SUM(cs.gross_revenue) 
                        FILTER (WHERE cs.state = 'COMPLETED')
                        , 
                        0
                ) AS total_revenue
                ,
                COALESCE(
                    SUM(cs.charge_duration_minutes)
                        FILTER (WHERE cs.state = 'COMPLETED')
                    , 
                    0
                ) AS charging_minutes
                ,
                COUNT(DISTINCT cs.evse_path) AS evse_count

            FROM charging_sessions_fact cs

            LEFT JOIN info_station s
                ON s.id = cs.station_id
                    AND s.user_id = cs.user_id

            WHERE cs.user_id = $1
                AND cs.start_ts >= $2
                AND cs.end_ts < $3

            GROUP BY cs.station_id
            """
        async with self.db.pool.acquire() as conn:
            return await conn.fetch(q, user_id, date_from, date_to)