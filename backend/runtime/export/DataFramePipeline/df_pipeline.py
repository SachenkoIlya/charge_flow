import pandas as pd
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from backend.utils.context.ctx import Ctx




class DataFramePipeline:
    def __init__(self, ctx:"Ctx"):
        self.ctx = ctx
    
    
    async def run(self, user_id:int) -> pd.DataFrame:
        self.ctx.logger.info(f"Run DataFramePipeline.run")
        
        self.ctx.logger.debug(f"Получею s3 key")
        rows = await self.ctx.db.run_export.get_s3_key(
            user_id=user_id,
            type_method=self.ctx.type_method,
            run_mode=self.ctx.run_mode,
            run_id=self.ctx.run_id,
        )

        res = {}
        for row in rows:
            task_id = row['id']
            s3_key = row['s3_key']
            
            df = await self.ctx.s3.download_parquet_s3_from_key(
                bucket='chargeflow', 
                key=s3_key
            )

            if df is not None:
                try:
                    df = DataFramePipeline.normalize_df(
                        df=df, 
                        operator=self.ctx.operator, 
                        user_id=user_id
                    )
                except Exception as e:
                    self.ctx.logger.error(f"Normalize error {s3_key}: {e}")
                    df = None
            
            res[task_id] = {
                'df': df,
                's3_key': s3_key,
                'is_error': df is None
            }
        return res
           

        


    @staticmethod
    def normalize_df(df: pd.DataFrame, operator: str, user_id: int) -> pd.DataFrame:
        
        if df.empty:
            return pd.DataFrame()
        
        df['operator'] = operator
        df['user_id'] = user_id

        # даты
        df['startTs'] = pd.to_datetime(df['startTs'], utc=True)
        df['endTs'] = pd.to_datetime(df['endTs'], utc=True)

        # деньги
        df['grossRevenue'] = pd.to_numeric(df['grossRevenue'], errors='coerce').fillna(0).round(2)
        df['partnerRevenue'] = pd.to_numeric(df['partnerRevenue'], errors='coerce').fillna(0).round(2)

        # энергия
        df['energyKwh'] = pd.to_numeric(df['energyKwh'], errors='coerce').round(3)

        # время
        df['durationMinutes'] = pd.to_numeric(df['durationMinutes'], errors='coerce').round(2)
        df['chargeDurationMinutes'] = pd.to_numeric(df['chargeDurationMinutes'], errors='coerce').round(2)

        # SOC
        df['socStart'] = pd.to_numeric(df['socStart'], errors='coerce').astype('Int64')
       

        df['currentSoc'] = pd.to_numeric(df['currentSoc'], errors='coerce')
        df['currentSoc'] = df['currentSoc'].round().fillna(0).astype(int)

        # delta
        df['soc_delta'] = df['currentSoc'] - df['socStart'].fillna(0)

        return DataFramePipeline.rename_cols(df)
    


    @staticmethod
    def rename_cols(df:pd.DataFrame) -> pd.DataFrame:
        return df.rename(columns={
            'id': 'session_id',
            'chargerName': 'charger_name',
            'evsePath': 'evse_path',
            'connectorType': 'connector_type',
            'evseType': 'evse_type',
            'startTs': 'start_ts',
            'endTs': 'end_ts',
            'durationMinutes': 'duration_minutes',
            'energyKwh': 'energy_kwh',
            'socStart': 'soc_start',
            'currentSoc': 'current_soc',
            'chargeDurationMinutes': 'charge_duration_minutes',
            'postChargeDurationMinutes': 'post_charge_duration_minutes',
            'grossRevenue': 'gross_revenue',
            'partnerRevenue': 'partner_revenue',
            'subscriberId': 'subscriber_id'
        })