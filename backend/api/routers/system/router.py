from pydantic import BaseModel

from backend.api.routers.dashboard.manager import ManagerSystem
from backend.api.routers.system.schemas import SystemSchema, EtlRunsResponseSchema
from backend.database.get_manager import get_current_token, get_system
from fastapi import APIRouter
from fastapi import Depends
from backend.services.admin_required import admin_required
from core.logger.logger import logger



router = APIRouter(prefix='/system', tags=['system'])


@router.post('/monitoring', response_model=EtlRunsResponseSchema)
async def create(
    data: SystemSchema,
    _: None = Depends(admin_required),
    system :  ManagerSystem=Depends(get_system)
):
    # тут редис дергаем апи если в редис есть то отдаем кеш если нет дергаем
    return await system.monitoring.determine_type(data.mode)

    # еслои прошли сюда сохраняем в кеш