import asyncio
import sys

from backend.database.base import Base  
from backend.utils.context.ctx import Ctx
from backend.utils.context.run_ctx import RunContext
from uuid import uuid4
from backend.users.users import Users
from datetime import datetime, timezone, timedelta
from backend.core.connection import Connect
from backend.utils.config.reports import ReportConfig




async def _firs_run(
        base_db: Base,
        operator: str,
        user_id: int,
        run_mode: str = 'first_run',
         
        
):
    try:
        await main(
            type_method='chargepoints', 
            operator=operator, 
            run_mode=run_mode, 
            base_db=base_db,
            user_id=user_id
        )
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'run_mode': run_mode
        }
    return {
        'status': 'success',
        'run_mode': run_mode,
        'error': None
    }



    
async def main(type_method: str, run_mode: str, operator: str,base_db: Base, user_id:int):
    combat_users = []
    now = datetime.now(timezone.utc)
    run_id = uuid4().hex
    
    ctx = Ctx(
        type_method=type_method,
        base_db=base_db,
        run_mode=run_mode,
        run_id=run_id,
        operator=operator
        )
    
    
    rows = await ctx.db.run_reposityry.get_users(user_id=user_id)
    users = [Users.from_db(row) for row in rows]
    
    for user in users:
        policy = ReportConfig.REPORT_POLICIES.get(operator).get(type_method)
        if not policy:
            continue
        
        # после mvp накрутить проверку подписки
        # накрутить is_allowed разрещена ли выгрузка учитывая подписку trial, paid, no_paid
        # проверяем last success
        # если нет возвращаем none 
        last_success_from_db = await ctx.db.run_reposityry.get_last_success(
            user_id=user.id,
            type_method=type_method,
            run_mode=run_mode,
            operator=user.operator
        )
        # проверяем послденюю дату, если None возвращаем 
        # дату первого запуска, котоорый указан в policy 'first_run_days_back'
        ready_last_success = ReportConfig.should_run(
            policy=policy,
            last_success_from_db=last_success_from_db, 
            now=now
        )
        if not ready_last_success:
            ctx.logger.debug(f"skip {user.full_name} |{type_method}| Нет ready_last_success.".upper())
            continue
        
        combat_users.append(RunContext(
            user=user,
            now=now,
            last_success=ready_last_success
        ))
    if not combat_users:
        return
    await Connect.pie_in_chunck(
            combat_users=combat_users,
            ctx=ctx,
        )
  