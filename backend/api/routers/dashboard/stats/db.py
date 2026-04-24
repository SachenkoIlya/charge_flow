from core.base_db import Base
from datetime import datetime

class StatsDB:
    def __init__(self, base_db: "Base"):
        self.db = base_db


    async def get_metrics(self, user_id:int, date_from: datetime, date_to: datetime):
        q = """
            SELECT 
                total_revenue,
                operator_revenue,
                average_bill,
                total_revenue - operator_revenue AS my_revenue,
                COALESCE(ROUND(operator_revenue / NULLIF(total_revenue, 0) * 100, 2),0) AS operator_percent,
                total_energy_kwh,
                success_sessions,
                total_sessions,
                total_users,
                avg_charge_time
            FROM (
                SELECT
                    COALESCE(
                        SUM(cs.gross_revenue)
                        FILTER (WHERE cs.state = 'COMPLETED'),
                    0) AS total_revenue,

                    COALESCE(
                        SUM(cs.gross_revenue - partner_revenue)
                        FILTER(WHERE cs.state = 'COMPLETED'),
                        0) AS operator_revenue,

                    COALESCE(
                        SUM(cs.energy_kwh)
                        FILTER(WHERE cs.state = 'COMPLETED')
                        ) AS total_energy_kwh,
                    
                    COALESCE(
                        SUM(cs.gross_revenue) 
                        FILTER (WHERE cs.state = 'COMPLETED')
                        /
                        NULLIF(
                            COUNT(*) FILTER (WHERE cs.state = 'COMPLETED'),
                            0
                        ),
                    0) AS average_bill,

                    COUNT(*) 
                    FILTER (WHERE cs.state = 'COMPLETED')
                    AS success_sessions,
                    
                    COUNT(*) AS total_sessions, 
                    
                    COUNT(DISTINCT cs.subscriber_id)
                    FILTER (WHERE cs.state = 'COMPLETED') AS total_users,

                    COALESCE(AVG(cs.charge_duration_minutes), 0) AS avg_charge_time
                FROM charging_sessions_fact cs
                    WHERE cs.user_id = $1
                        AND cs.start_ts >= $2
                        AND cs.start_ts < $3
            ) t
           
            """
        async with self.db.pool.acquire() as conn:
            return await conn.fetchrow(q, user_id, date_from, date_to)
    
    async def get_data_chart(self, user_id: int, date_from: datetime, date_to: datetime):
        q = """
            SELECT 
                s.location_name AS name,
                COALESCE(SUM(cs.gross_revenue), 0) as value
            FROM info_station_test s
            
            LEFT JOIN charging_sessions_fact as cs
                ON split_part(cs.evse_path, '/', 1) = s.key
                AND cs.user_id = $1
                AND cs.start_ts BETWEEN $2 AND $3
                
            WHERE s.location_name IS NOT NULL 
                AND s.user_id = $1

            GROUP BY s.location_name
            ORDER BY value DESC
            """
        async with self.db.pool.acquire() as conn:
            return await conn.fetch(q, user_id, date_from, date_to)
        
    async def get_total_station(self, user_id):
        q = """
            SELECT COUNT(DISTINCT  s.station_id) AS total_station
            FROM info_station_test s
                WHERE s.user_id = $1
            """
        async with self.db.pool.acquire() as conn:
            return await conn.fetchrow(q, user_id)