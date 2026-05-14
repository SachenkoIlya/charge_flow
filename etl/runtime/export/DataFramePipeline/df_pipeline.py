import pandas as pd
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from etl.utils.context.ctx import Ctx

from core.logger.logger import logger


class DataFramePipeline:
    def __init__(self, ctx:"Ctx"):
        self.ctx = ctx
        self.BUCKET= 'chargeflow'
    
    async def run(self, user_id:int) -> pd.DataFrame:
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
                bucket=self.BUCKET, 
                key=s3_key
            )

            if df is not None:
                try:
                    df = DataFramePipeline.normalize_df(
                        df=df, 
                        operator=self.ctx.operator,
                        type_method=self.ctx.type_method, 
                        user_id=user_id
                    )
                except Exception as e:
                    logger.error(f"Normalize error {s3_key}: {e}")
                    df = None
            
            res[task_id] = {
                'df': df,
                's3_key': s3_key,
                'is_error': df is None
            }
        return res
           

        
   

    @staticmethod
    def normalize_df(df: pd.DataFrame, operator: str,type_method:str, user_id: int) -> pd.DataFrame:
        
        if df.empty:
            return pd.DataFrame()

        df['operator'] = operator
        df['user_id'] = user_id

        if type_method == 'chargepoints':
            df = df.where(pd.notnull(df), None)
            df["lastSeen"] = pd.to_datetime(
                df["lastSeen"],
                utc=True,
            )
            return df
        
        # даты
        df["start_ts"] = pd.to_datetime(df["start_ts"], utc=True)
        df["end_ts"] = pd.to_datetime(df["end_ts"], utc=True)
        # деньги
        df["gross_revenue"] = (
            pd.to_numeric(df["gross_revenue"], errors="coerce")
            .fillna(0)
            .round(2)
        )

        df["partner_revenue"] = (
            pd.to_numeric(df["partner_revenue"], errors="coerce")
            .fillna(0)
            .round(2)
        )

        # энергия
        df["energy_kwh"] = (
            pd.to_numeric(df["energy_kwh"], errors="coerce")
            .round(3)
        )
        # время
        df["duration_minutes"] = (
            pd.to_numeric(df["duration_minutes"], errors="coerce")
            .round(2)
        )
        df["charge_duration_minutes"] = (
            pd.to_numeric(df["charge_duration_minutes"], errors="coerce")
            .round(2)
        )
        # SOC
        df["soc_start"] = (
            pd.to_numeric(df["soc_start"], errors="coerce")
            .astype("Int64")
        )
        df["current_soc"] = (
            pd.to_numeric(df["current_soc"], errors="coerce")
            .round()
            .fillna(0)
            .astype(int)
        )
        df["soc_delta"] = (
            df["current_soc"] - df["soc_start"].fillna(0)
        )
        return df
    

