from dataclasses import dataclass
from copy import deepcopy   
import aiohttp
from datetime import datetime, timezone
import traceback
import json

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from backend.utils.context.ctx import Ctx
    from backend.utils.context.run_ctx import RunContext


@dataclass
class Universal:
    body: dict
    url: str
    method: str
    type_method: str
    


    async def get_data(self, sess: aiohttp.ClientSession, run_ctx: "RunContext", ctx:"Ctx"):
        start_run = datetime.now(timezone.utc)
        
        ctx.logger.debug(f"start_date = {run_ctx.now}")
        ctx.logger.debug(f"last_success = {run_ctx.last_success}")
       
        error = []
        result = []
        body = deepcopy(self.body)

        cnt = 0
        response = None
        while True:
            try:
                response = await ctx.work_spase.request_to_marketplace(
                    user=run_ctx.user,
                    sessions=sess,
                    body=body,
                    data={
                        'method': self.method,
                        'url': self.url,
                        'type_method': self.type_method,
                    },
                )
            except Exception as e:
                ctx.logger.error(traceback.format_exc())
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
                ctx.logger.debug(
                    f"user: {run_ctx.user.full_name}\n"
                    f"new_data: {len(new_data)}\n"
                    f"page={cnt} newest={response[0]['startTs']} oldest={response[-1]['startTs']}"
                )

                if not new_data:
                    break
                
                result.extend(new_data)
                ctx.logger.debug(f"[{run_ctx.user.full_name}]len result: {len(result)}")
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
        )

