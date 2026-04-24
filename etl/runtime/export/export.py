from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from etl.utils.context.run_ctx import RunContext
    from etl.utils.context.ctx import Ctx
    from etl.users.users import Users

from datetime import datetime, timezone
import asyncio 



class ExportFromBi:
    
    @staticmethod
    async def run_export_task(ctx:"Ctx", run_contexts: list["RunContext"]):
        tasks = [
            ExportFromBi._run_export(user=run_ctx.user, ctx=ctx)
            for run_ctx in run_contexts
        ]

        if not tasks:
            ctx.logger.warning(f"нет тасок, прекращаем выполнение")
            return 
        
        start = datetime.now(timezone.utc)
        result = await asyncio.gather(*tasks, return_exceptions=True)
        end = datetime.now(timezone.utc)
        
        duration = (end - start).total_seconds()
        ctx.logger.info(f"run_export_task выполнен за {duration:.2f} сек")
        
        for run_ctx, res, in zip(run_contexts, result):
            if isinstance(res, Exception):
                ctx.logger.error(f"{run_ctx.user.full_name}: {res}")



    @staticmethod
    async def _run_export(user:"Users", ctx:"Ctx"):
        export = {
            'charging_sessions': ctx.db.run_export.insert_charging_sessions_df,
            'chargepoints': ctx.db.run_export.insert_chargepoints_df,
        }
        ctx.logger.info(f"{user.full_name}: запуск df_flow.run")
        try:
            tasks_ids = await ctx.df_flow.run(
                user_id=user.id,
            )
            for task_id, data in tasks_ids.items():
                if data['is_error']:
                    await ctx.db.run_export.update_bi_exports(task_id, 'error')
                    continue
                
                df = data['df']
                if df.empty:
                    await ctx.db.run_export.update_bi_exports(task_id, 'skipped')
                    continue
                
                ctx.logger.debug(f"{user.full_name} | Запускаю:{export[ctx.type_method]}")
                await export[ctx.type_method](df, ctx.run_mode)
                await ctx.db.run_export.update_bi_exports(task_id, 'success')
        except Exception as e:
            ctx.logger.exception(f"{user.full_name}: ошибка в _run_export")
            raise e