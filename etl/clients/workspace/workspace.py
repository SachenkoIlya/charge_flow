from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.storage.client import S3Client

from etl.clients.workspace.config import get_parser
from etl.users.users import Users
from core.logger.logger import logger

from datetime import datetime
import pandas as pd
import traceback



class WorkSpase:
    async def work_data(
        self, 
        user: "Users", 
        api_meta: dict, 
        result:list[dict], 
        type_method, now: datetime, 
        operator:str,
        api_error:list=None,
        s3: "S3Client"=None,
        run_id: str=None,
        mask:str = '%Y-%m-%dT%H:%M:%SZ'    
    ) -> dict:
        all_meta = {
            'pipeline_data': None,
            "api_meta": api_meta,
            'parser_meta': None,
            'storage_meta': None,
            'error': []
        }
        all_meta['pipeline_data'] = {
            'next_last_success': now.strftime(mask)
        }
        
        if api_error:
            all_meta["api_meta"]["status"] = 'error'
            all_meta['error'].extend(api_error)
            return all_meta
        if not result:
            logger.info(f"Пустой result.{type_method} — сохраняю дкфолтный empty. выход")
            all_meta["api_meta"]["status"] = 'empty'
            return all_meta 
        
        try:
            all_meta['api_meta']['status'] = 'success'

            min_date = None
            max_date = None
            
            if type_method == 'charging_sessions':
                dates = [
                    datetime.fromisoformat(r['startTs'].replace("Z", "+00:00") )
                    for r in result
                ]
                if dates:
                    min_date = min(dates)
                    max_date = max(dates)
            
            parser = get_parser(operator, type_method)
            df:pd.DataFrame = parser.to_df(result)
           
            all_meta['parser_meta'] = {
                "status": 'success',
                "rows": df.shape[0],
                "cols": df.shape[1],
                "min_date": min_date.strftime(mask) if min_date else None,
                "max_date": max_date.strftime(mask) if max_date else None,
                "memory_usage": df.memory_usage(deep=True).sum() / 1024**2
            }
            
            if s3 is None:
                raise ValueError("s3 client is required")
            
            storage = await s3.upload_parquet_and_get_url(
                user_id=user.id,
                run_id=run_id,
                type_method=type_method,
                df=df, 
            )
            all_meta['storage_meta'] = {
                "status": 'success', 
                "key": storage[0],
                "compression": storage[1],
                "size_parquet_kb":storage[2],
            }
        except Exception as e:
            logger.error(traceback.format_exc())
            all_meta['error'].append({
                'status': 'error',
                'error': str(e),
                'logs': f"Ошибка в работе work data",
                'error_type': type(e).__name__ 
            })
            return all_meta
        return all_meta