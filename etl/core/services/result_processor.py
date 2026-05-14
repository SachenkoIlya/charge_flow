from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from etl.utils.context.run_ctx import RunContext
    from etl.utils.context.ctx import Ctx
    from database.manager import Manager
  
from etl.core.config import get_export_task
from core.security.settings import settings
import traceback
from core.logger.logger import logger
from dataclasses import dataclass

@dataclass
class PipelineResultProcessor:
    ctx: "Ctx"
    run_contexts: "RunContext"


    async def launch_exp(self):
        scenario_exp = get_export_task(
            operator=self.ctx.operator,
            type_method=self.ctx.type_method
        )
        if not scenario_exp:
            logger.warning(f"Нет сценария для {self.ctx.operator}:{self.ctx.type_method}")
            return
        logger.info(f"Запускаю scenario_exp для {self.ctx.type_method}".upper())
        await scenario_exp(ctx=self.ctx, run_contexts=self.run_contexts)
    
    @staticmethod 
    def normalize_meta(exc: Exception) ->dict:
            return  {
            'pipeline_data': None,
            "api_meta": None,
            'parser_meta': None,
            'storage_meta': None,
            'error': [
                {
                    "type": type(exc).__name__,
                    "message": str(exc),
                }
            ],
        }

    @staticmethod
    def resolve_status(meta: dict) -> str:
        if meta.get('error'):
            return 'error'
        
        api_meta = meta.get("api_meta") or {}
        if api_meta.get("status") == "empty":
            return "empty"
        return "success"
    
    async def process(
        self,
        result, 
    ) -> None:
        
        for run_ctx, raw_meta in zip(self.run_contexts, result):
            all_meta = (
                self.normalize_meta(raw_meta)
                if isinstance(raw_meta, Exception)
                else raw_meta
            )

            status = self.resolve_status(meta=all_meta)
            try:
                await self.ctx.db.run_piplines.insert(
                    user_id=run_ctx.user.id,
                    operator=run_ctx.user.operator,
                    type_method=self.ctx.type_method,
                    run_mode=self.ctx.run_mode,
                    run_id=self.ctx.run_id,
                    status=status,
                    last_success_at=run_ctx.now,
                    meta=all_meta
                )
                logger.info(f"Данные записаны в бд run_piplines".upper())
            except Exception as e:
                logger.warning(run_ctx.user.full_name)
                logger.error(f"{run_ctx.full_name}: {str(e)}\n\n")
                if settings.MODE in {'test', 'dev'}:
                    logger.error(traceback.format_exc())

            if status == 'success':
                s3_key = all_meta['storage_meta']['key']
                try:    
                    await self.ctx.db.run_export.insert_bi_export_task(
                        user_id=run_ctx.user.id,
                        operator=run_ctx.user.operator,
                        run_mode=self.ctx.run_mode,
                        type_method=self.ctx.type_method,
                        run_id=self.ctx.run_id,
                        s3_key=s3_key
                    )
                    logger.info(f"Данные записаны в бд bi_export".upper())
                except Exception as e:
                    if settings.MODE in {'test', 'dev'}:
                        logger.error(traceback.format_exc())
            
        await self.launch_exp()