from backend.database.base import Base
from backend.utils.logger.logger import make_logger
import json
import pandas as pd
logger = make_logger(__name__, use_telegram=False)


class RunExport:
    def __init__(self, base_db: Base):
        self.db = base_db

    
    @Base.with_retries(retries=5, delay=1.5, msg_prefix='RunExport.get_s3_key')
    async def get_s3_key(self, user_id:int, type_method:str, run_mode:'str', run_id: str):

        q = """
            UPDATE bi_exports
            SET status = 'processing'
            WHERE id IN (
                SELECT id
                FROM bi_exports
                 WHERE status = 'pending'
                AND user_id = $1
                AND type_method = $2
                AND run_mode = $3 
                AND run_id = $4
            ORDER BY created_at 
            limit 100
            FOR UPDATE SKIP LOCKED
            )
            RETURNING id, s3_key;
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



    @Base.with_retries(retries=5, delay=1.5, msg_prefix='RunExport.insert_df')
    async def insert_df(self, df:pd.DataFrame, run_mode: str):
        
        table = 'charging_sessions_fact'

        if run_mode == 'test':
            table = 'charging_sessions_fact_test'
            

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
                charger_name, evse_path , state, connector_type, evse_type, reason,
                start_ts, end_ts, duration_minutes, energy_kwh,
                charge_duration_minutes, post_charge_duration_minutes,
                gross_revenue, partner_revenue,
                soc_start, current_soc, soc_delta
            )
            VALUES (
                $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,
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
