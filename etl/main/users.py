
from etl.main.schemas import RunContextMeta
from etl.users.users import UserCredentials
from etl.utils.config.reports import ReportConfig
from etl.utils.context.ctx import Ctx
from etl.utils.context.run_ctx import RunContext



async def build_users(ctx: "Ctx", meta: "RunContextMeta"):
    rows = await ctx.db.run_reposityry.get_users()
    users = [UserCredentials.from_db(row) for row in rows]
    
    run_context = []
    for user in users:
        policy = ReportConfig.REPORT_POLICIES.get(ctx.operator).get(ctx.type_method)
        if not policy:
            continue
        
        # после mvp накрутить проверку подписки
        # накрутить is_allowed разрещена ли выгрузка учитывая подписку trial, paid, no_paid
        # проверяем last success
        # если нет возвращаем none 
        last_success_from_db = await ctx.db.run_reposityry.get_last_success(
            user_id=user.id,
            type_method=ctx.type_method,
            run_mode=ctx.run_mode,
            operator=user.operator
        )
        # проверяем послденюю дату, если None возвращаем 
        # дату первого запуска, котоорый указан в policy 'first_run_days_back'
        ready_last_success = ReportConfig.should_run(
            policy=policy,
            last_success_from_db=last_success_from_db, 
            now=meta.started_at
        )
        if not ready_last_success:
            ctx.logger.debug(
                f"skip {user.full_name} |{ctx.type_method}| Нет ready_last_success.".upper()
            )
            ctx.logger.debug(f"ready_last_success: {ready_last_success}".upper())
            continue
        
        run_context.append(RunContext(
            user=user,
            now=meta.started_at,
            last_success=ready_last_success
        ))
    if not run_context:
        return []
    return run_context
