from core.logger.logger import make_logger
from core.config.config import get_table_name_map, CHARGEPOINTS, CHARGIN_SESSION
from core.base_db import Base
import pandas as pd

logger = make_logger(__name__, use_telegram=False)

class RunExport:
    def __init__(self, base_db: Base):
        self.db = base_db
        self.tables = {
            'info_station': {
                "dev": "info_station_test",
                "test": "info_station_test",
                "prod": "info_station",
            },

            'charging_sessions': {
                "dev": "charging_sessions_fact_test",
                "test": "charging_sessions_fact_test",
                "prod": "charging_sessions_fact",
            },
        }

    @staticmethod
    def _get_table_name(point: str):
        return get_table_name_map(point)


    @Base.with_retries(retries=5, delay=1.5, msg_prefix='RunExport.get_s3_key')
    async def get_s3_key(self, user_id:int, type_method:str, run_mode:'str', run_id: str):
        q = """
            WITH cte AS (
                SELECT id 
                FROM bi_exports
                WHERE user_id = $1
                AND (
                    status = 'pending' OR (
                        status = 'processing'
                        AND updated_at < NOW() - INTERVAL '10 minutes'
                    )
                )
                AND type_method = $2
                AND run_mode = $3 
                AND run_id = $4
                ORDER BY created_at
                LIMIT 100
                FOR UPDATE SKIP LOCKED
            )
            UPDATE bi_exports b 
            SET status = 'processing',
                updated_at = NOW()
            FROM cte
            WHERE b.id = cte.id 
            RETURNING b.id, b.s3_key;
            """
        async with self.db.pool.acquire() as conn:
            rows = await conn.fetch(
                q, 
                user_id, 
                type_method, 
                run_mode, 
                run_id
            )
        return rows

    @Base.with_retries(retries=5, delay=1.5, msg_prefix='RunExport.insert_chargepoints_df')
    async def insert_chargepoints_df(self, df:pd.DataFrame, run_mode: str):
        table = self._get_table_name(CHARGEPOINTS)
        
        columns = [
            'user_id', 'operator',
            "station_id", "key", "name", "serialNumber",
            "state", "connected", "lastSeen", "location_id",
            "location_name", "location_address", "location_city", 
            "location_latitude", "location_longitude", "model", 
            "vendor", "protocol", "operatorId", "operatorName"
        ]
        df = df[columns]

        q = f"""
            INSERT INTO {table} (
                user_id, operator,
                station_id, key, name, serialNumber,
                state, connected, lastSeen, location_id,
                location_name, location_address, location_city, 
                location_latitude, location_longitude, model, 
                vendor, protocol, operatorId, operatorName
            )
            VALUES (
                $1, $2, $3, $4, $5, $6, $7, $8, $9, $10,
                $11, $12, $13, $14, $15, $16, $17, $18, $19, $20
            )
            ON CONFLICT (station_id)

            DO UPDATE SET
                station_id=EXCLUDED.station_id,
                key=EXCLUDED.key, 
                name=EXCLUDED.name, 
                serialNumber=EXCLUDED.serialNumber,
                state=EXCLUDED.state, 
                connected=EXCLUDED.connected, 
                lastSeen=EXCLUDED.lastSeen, 
                location_id=EXCLUDED.location_id,
                location_name=EXCLUDED.location_name, 
                location_address=EXCLUDED.location_address, 
                location_city=EXCLUDED.location_city, 
                location_latitude=EXCLUDED.location_latitude, 
                location_longitude=EXCLUDED.location_longitude, 
                model=EXCLUDED.model, 
                vendor=EXCLUDED.vendor, 
                protocol=EXCLUDED.protocol, 
                operatorId=EXCLUDED.operatorId, 
                operatorName=EXCLUDED.operatorName;
            """
        records = [
            tuple(None if pd.isna(v) else v for v in row)
            for row in df.to_numpy()
        ]
        async with self.db.pool.acquire() as conn:
            await conn.executemany(q, records)


    @Base.with_retries(retries=5, delay=1.5, msg_prefix='RunExport.insert_charging_sessions_df')
    async def insert_charging_sessions_df(self, df:pd.DataFrame, run_mode: str):
        table = self._get_table_name(CHARGIN_SESSION)
        table_charge_points = self._get_table_name(CHARGEPOINTS)
        columns = [
            'session_id','contract','subscriber_id','user_id','operator',
            'charger_name','evse_path','state','connector_type','evse_type','reason',
            'start_ts','end_ts','duration_minutes','energy_kwh',
            'charge_duration_minutes','post_charge_duration_minutes',
            'gross_revenue','partner_revenue',
            'soc_start','current_soc','soc_delta'
        ]
        df = df[columns]


        q = f"""
            INSERT INTO {table} (
                session_id, contract, subscriber_id, user_id, operator,
                charger_name, evse_path, station_id, state, connector_type, evse_type, reason,
                start_ts, end_ts, duration_minutes, energy_kwh,
                charge_duration_minutes, post_charge_duration_minutes,
                gross_revenue, partner_revenue,
                soc_start, current_soc, soc_delta
            )
            VALUES (
                $1,$2,$3,$4,$5,$6,$7,
                (
                    SELECT c.id
                    FROM {table_charge_points} c
                    WHERE c.operator = $5
                        AND c.key = split_part($7, '/', 1)
                    LIMIT 1
                ),
                $8,$9,$10,$11,
                $12,$13,$14,$15,$16,$17,$18,$19,$20,$21,$22
            )
           
            ON CONFLICT (session_id) DO NOTHING;
        """
        records = [
            tuple(None if pd.isna(v) else v for v in row)
            for row in df.to_numpy()
        ]
        async with self.db.pool.acquire() as conn:
            await conn.executemany(q, records)


    @Base.with_retries(retries=5, delay=1.5, msg_prefix='insert_bi_export_task')
    async def insert_bi_export_task(
        self, 
        user_id: int, 
        operator: str, 
        run_mode: str,
        type_method: str, 
        run_id:str, 
        s3_key:str
    ):
        q = """
            INSERT INTO bi_exports(
                user_id, 
                operator, 
                run_mode,
                type_method, 
                run_id, 
                s3_key
            ) 
            VALUES(
                $1, $2, $3, $4, $5, $6
            )
            """
        async with self.db.pool.acquire() as conn:
            await conn.execute(
                q, 
                user_id, 
                operator, 
                run_mode,
                type_method, 
                run_id, 
                s3_key
            )
    
    
    @Base.with_retries(retries=5, delay=1.5, msg_prefix='update_bi_exports')
    async def update_bi_exports(self, tasks_id: int, status: 'str'):
        q = """
            UPDATE bi_exports
            SET status = $1
            WHERE id = $2
            """

        async with self.db.pool.acquire() as conn:
            result = await conn.execute(
                q,
                status,
                tasks_id
            )

            logger.info(result)


