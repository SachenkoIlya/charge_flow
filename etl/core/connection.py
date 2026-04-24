from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from etl.utils.context.run_ctx import RunContext
    from etl.utils.context.ctx import Ctx

from etl.clients.volt.regstry import RegstryVolt
from etl.runtime.export.export import ExportFromBi

import traceback
import asyncio
import aiohttp

class Connect:
    map_cls = {
        'volt': RegstryVolt
    }

    map_scenario_export = {
        'bi': {
            'volt': {
                'charging_sessions': ExportFromBi.run_export_task,
                'chargepoints': ExportFromBi.run_export_task
            }
            
        }
    }

    @staticmethod   
    async def _connect_aiohttp(func, *args, **kwargs):
        connector = aiohttp.TCPConnector(limit=50, limit_per_host=4, ttl_dns_cache=120)
        timeout = aiohttp.ClientTimeout(total=None, connect=40, sock_connect=30, sock_read=120)

        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as sess:
            await func(sess, *args, **kwargs)





    @staticmethod
    async def pie_in_chunck(combat_users:list["RunContext"], ctx: "Ctx"):
        # region DOC:
        """
        Запускает обработку отчётов по магазинам батчами (чанками),
        чтобы ограничить нагрузку на систему и внешние сервисы.

        Логика работы:
        1. В ctx.meta.count_cabinets сохраняется общее количество магазинов,
           переданных на обработку.
        2. Список store_context разбивается на чанки фиксированного размера (по 20).
        3. Для каждого чанка вызывается асинхронный запуск пайплайнов
           через BaseCore._connect_aiohttp.
        4. После обработки каждого чанка выполняется пауза (60 секунд),
           чтобы избежать перегрузки API, БД или внешних источников данных.

        Это позволяет:
        - контролировать параллелизм,
        - снижать пиковую нагрузку,
        - соблюдать rate limits внешних сервисов.

        :param store_context: Список контекстов запуска для магазинов.
        :param ctx: Общий контекст выполнения отчёта.
        :param report_name: Название отчёта, который необходимо построить.
        """
        # endregion
        chunck = 20
        for i in range(0, len(combat_users), chunck):
            chunck_size = combat_users[i:i+chunck]
            await Connect._connect_aiohttp(
                Connect.run_pipelines,
                run_contexts=chunck_size,
                ctx=ctx,
            )

            if i + chunck < len(combat_users):
                await asyncio.sleep(60)



    @staticmethod
    async def run_pipelines(sess:aiohttp.ClientSession, run_contexts: list["RunContext"], ctx:"Ctx"):

        report = Connect.map_cls[ctx.operator].registry[ctx.type_method]

        tasks = [
            report.get_data(sess=sess, run_ctx=run_ctx, ctx=ctx)
            for run_ctx in run_contexts
        ]
        
        if not tasks:
            ctx.logger.warning(f"нет тасок для {ctx.type_method}")
            return
        
        result = await asyncio.gather(*tasks, return_exceptions=True)
        
        for run_ctx, all_meta in zip(run_contexts, result):
            if isinstance(all_meta, Exception):
                ctx.logger.exception(f"❌ Ошибка в задаче {run_ctx}: {all_meta}")
                status = 'error'
            
            if all_meta['error']:
                status = 'error'
            elif all_meta['api_meta'].get('status') == 'empty':
                status = 'empty'
            else:
                status = 'success'
            
            try:
                await ctx.db.run_piplines.insert(
                    user_id=run_ctx.user.id,
                    operator=run_ctx.user.operator,
                    type_method=ctx.type_method,
                    run_mode=ctx.run_mode,
                    run_id=ctx.run_id,
                    status=status,
                    last_success_at=run_ctx.now,
                    meta=all_meta
                )
                ctx.logger.info(f"Данные записаны в бд run_piplines".upper())
                
            except Exception as e:
                ctx.logger.warning(run_ctx.user.full_name)
                ctx.logger.warning(f"Ощибка записи meta в ctx.db.run_piplines.insert".upper())
                ctx.logger.error(f"{str(e)}\n\n")
                ctx.logger.error(traceback.format_exc())

            # if ctx.type_method == 'chargepoints':
            #     ctx.logger.warning(f"временный пропуск: {ctx.type_method}")
            #     continue
            
            if status == 'success':
                s3_key = all_meta['storage_meta']['key']
                try:
                    await ctx.db.run_export.insert_bi_export_task(
                        user_id=run_ctx.user.id,
                        operator=run_ctx.user.operator,
                        run_mode=ctx.run_mode,
                        type_method=ctx.type_method,
                        run_id=ctx.run_id,
                        s3_key=s3_key
                    )
                    ctx.logger.info(f"Данные записаны в бд bi_export".upper())
                except Exception as e:
                    ctx.logger.warning(run_ctx.user.full_name)
                    ctx.logger.warning(f"Ощибка записи meta в insert_bi_export_task".upper())
                    ctx.logger.error(f"{str(e)}\n\n")
                    ctx.logger.error(traceback.format_exc())
        
        scenario_exp =  Connect.map_scenario_export.get('bi', {})\
            .get(ctx.operator, {})\
            .get(ctx.type_method)
        
        if not scenario_exp:
            ctx.logger.warning(f"Нет сценария для {ctx.operator}:{ctx.type_method}")
            return
            
        ctx.logger.info(f"Запускаю scenario_exp для {ctx.type_method}".upper())
        await scenario_exp(ctx=ctx, run_contexts=run_contexts)






      
        


