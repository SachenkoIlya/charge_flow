from etl.utils.config.reports import ReportConfig
from etl.utils.context.run_ctx import RunContext
from etl.core.connection import Connect
from etl.utils.context.ctx import Ctx
from etl.users.users import UserCredentials

from datetime import datetime, timezone
from core.base_db import Base
from dotenv import load_dotenv
from uuid import uuid4
import asyncio
import sys
import os
load_dotenv()

    
    
async def run_all_endpoints(run_mode: str, operator: str):
    base_db = Base()
    print(f"{run_mode}, {operator}")
    await base_db.connect()
    try:
        for type_method in ReportConfig.TYPE_METHODS.get(operator):
            # if type_method == 'charging_sessions':
            #     continue
            await main(
                type_method=type_method, 
                operator=operator, 
                run_mode=run_mode, 
                base_db=base_db
            )
    finally:
        await base_db.close()



async def main(type_method: str, run_mode: str, operator: str, base_db: "Base", user_id: int = None):
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
    
    
    rows = await ctx.db.run_reposityry.get_users()
    users = [UserCredentials.from_db(row) for row in rows]
    
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
  




if __name__ == '__main__':
    # py -m etl.main.main volt
    # py -m etl.main.main scheduled volt
    import sys

    if len(sys.argv) < 1:
        raise RuntimeError("operator is required")
    run_mode = os.getenv('RUN_MODE', 'test')
    operator = sys.argv[1]
    
    asyncio.run(run_all_endpoints(run_mode, operator))   
    