from etl.clients.volt.universal.parser import Parser as volt_parser

from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from etl.utils.context.ctx import Ctx   

from etl.users.users import Users
from datetime import datetime
import pandas as pd
import traceback
import aiohttp
import json


class WorkSpase:
    PARSER = {
        'volt': {
            'chargepoints': volt_parser,
            'charging_sessions': volt_parser,
        },
        'sitronics': {
            'default': 'default'
        }
    }

    def __init__(self, ctx: "Ctx"):
        self.ctx = ctx
    
    
    async def request_to_marketplace(
            self, user: Optional["Users"], 
            sessions: aiohttp.ClientSession, 
            data: dict, body:dict
        )-> json:
        
        return await self.ctx.request(
                sessions=sessions,
                user=user,
                type_method=data['type_method'],
                method=data['method'],
                url=data['url'],
                body=body,
            )
    
    async def work_data(
            self, 
            user: "Users", 
            api_meta: dict, 
            result:list[dict], 
            type_method, now: datetime, 
            api_error:list=None,
    ):
        all_meta = {
            'pipeline_data': None,
            "api_meta": api_meta,
            'parser_meta': None,
            'storage_meta': None,
            'error': []
        }
        all_meta['pipeline_data'] = {
            'next_last_success': now.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        
        if api_error:
            all_meta["api_meta"]["status"] = 'error'
            all_meta['error'].extend(api_error)
            return all_meta
        if not result:
            self.ctx.logger.info(f"Пустой result.{type_method} — сохраняю дкфолтный empty. выход")
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
            
            parser = self.PARSER.get(user.operator).get(type_method)
            df:pd.DataFrame = parser.to_df(result, type_method)
           
            all_meta['parser_meta'] = {
                "status": 'success',
                "rows": df.shape[0],
                "cols": df.shape[1],
                "min_date": min_date.strftime("%Y-%m-%dT%H:%M:%SZ") if min_date else None,
                "max_date": max_date.strftime("%Y-%m-%dT%H:%M:%SZ") if max_date else None,
                "memory_usage": df.memory_usage(deep=True).sum() / 1024**2
            }
            
            storage = await self.ctx.s3.upload_parquet_and_get_url(
                user_id=user.id,
                run_id=self.ctx.run_id,
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
            self.ctx.logger.error(traceback.format_exc())
            all_meta['error'].append({
                'status': 'error',
                'error': str(e),
                'logs': f"Ошибка в работе work data",
                'error_type': type(e).__name__ 
            })
            return all_meta
        
        return all_meta