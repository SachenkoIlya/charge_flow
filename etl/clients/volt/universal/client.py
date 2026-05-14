from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from etl.utils.context.ctx import Ctx
    from etl.utils.context.run_ctx import RunContext

from datetime import datetime, timezone
from dataclasses import dataclass
from copy import deepcopy   
import traceback
from core.logger.logger import logger

@dataclass
class BaseVoltApi:
    body: dict
    url: str
    method: str
    type_method: str
    
    async def get_data(self, run_ctx: "RunContext", ctx:"Ctx"):
        start_run = datetime.now(timezone.utc)
        body = deepcopy(self.body)
        error,result = [], []
        cnt = 0
        response = None
        
        while True:
            try:
                ctx.logger.info(
                    f"[VOLT REQUEST] user={run_ctx.user.id}/{run_ctx.user.full_name} "
                    f"type={ctx.type_method} "
                    f"from={body.get('from')} "
                    f"to={body.get('to')} "
                    f"offset={body.get('offset')} "
                    f"limit={body.get('limit')}"
                )

                if self.method == 'get':
                    response = await ctx.aiohttp_client.get(
                        auth_type=run_ctx.user.auth_type,
                        url=self.url,
                        payload=body,
                        login=run_ctx.user.login,
                        password=run_ctx.user.password,
                        use_rate_limit=True
                    )
            except Exception as e:
                logger.error(traceback.format_exc())
                error.append({
                    "status": "error",
                    "page": cnt,
                    "offset": body["offset"],
                    "error": str(e),
                    "time": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                })
                break

            if not response:
                break
            
            cnt += 1
            body["offset"] += body.get("limit", 50)

            if self.type_method == 'charging_sessions':
                new_data = [
                    r for r in response
                    if datetime.fromisoformat(r["startTs"].replace("Z", "+00:00")) > run_ctx.last_success
                ]
                if not new_data:
                    break
                
                result.extend(new_data)
            else:
                result.extend(response)

        api_meta = {
            'start_run': start_run.strftime("%Y-%m-%dT%H:%M:%SZ"),
            'status':None,
            "pages": cnt,
            'finished_run': datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        }

        return await ctx.work_spase.work_data(
            user=run_ctx.user,
            api_meta=api_meta,
            result=result,
            api_error=error,
            type_method=self.type_method,
            now=run_ctx.now,
            s3=ctx.s3,
            run_id=ctx.run_id,
            operator=ctx.operator
        )

