from typing import TYPE_CHECKING

from etl.core.services.result_processor import PipelineResultProcessor
if TYPE_CHECKING:
    from etl.utils.context.run_ctx import RunContext
    from etl.utils.context.ctx import Ctx

from etl.core.config import get_registry_report

import asyncio
import aiohttp




class RunPipelines:
   
    async def _run(self, run_context:list["RunContext"], ctx: "Ctx"):
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
        sem = asyncio.Semaphore(5)
        await self.run_pipelines(
            run_contexts=run_context,
            ctx=ctx,
            sem=sem
        )
    
    async def run_pipelines(
        self, 
        run_contexts: list["RunContext"], 
        ctx:"Ctx", 
        sem:asyncio.Semaphore
    ):

        # report = MAP_CLS[ctx.operator].registry[ctx.type_method]
        cls_registry = get_registry_report(ctx.operator)
        method = cls_registry.registry.get(ctx.type_method)
        
        async def run_one(run_ctx):
            async with sem:
                return await method.get_data(
                    run_ctx=run_ctx, 
                    ctx=ctx
                )
            
        tasks = [
            run_one(run_ctx) 
            for run_ctx in  run_contexts
        ]
        
        if not tasks:
            ctx.logger.warning(f"нет тасок для {ctx.type_method}")
            return
        
        result = await asyncio.gather(*tasks, return_exceptions=True)
        post_processor = PipelineResultProcessor(ctx, run_contexts)
        await post_processor.process(result)




      
        


