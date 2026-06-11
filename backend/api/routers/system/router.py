from pydantic import BaseModel

from backend.api.routers.dashboard.manager import ManagerSystem
from backend.api.routers.system.schemas import SystemSchema, EtlRunsResponseSchema
from backend.dependencies.get_manager import get_system
from fastapi import APIRouter
from fastapi import Depends
from backend.services.admin_required import admin_required

ENDPOINT = '/monitoring'
DESCRIPTIONS =  """ 
    Возвращает данные мониторинга внутренних сервисов ChargeFlow.
    Поддерживаемые режимы:
        - `etl_run` — история запусков ETL-процессов;
        - `bi_exports` — история выгрузок BI-отчётов.

        Доступно только администраторам системы.

        Используется для отображения состояния фоновых процессов,
        контроля ошибок и анализа выполненных задач.
"""
router = APIRouter(prefix='/v1/system', tags=['system'])

@router.post(
    ENDPOINT, 
    monitoring="Получить данные мониторинга системы",
    description=DESCRIPTIONS,
    response_model=EtlRunsResponseSchema
)
async def create(
    data: SystemSchema,
    _: None = Depends(admin_required),
    system :  ManagerSystem=Depends(get_system)
):  
    """
    Получить данные мониторинга.

    Args:
        data (SystemSchema):
            Параметры запроса мониторинга.

        _:
            Проверка прав администратора.

        system (ManagerSystem):
            Менеджер системных сервисов.

    Returns:
        EtlRunsResponseSchema:
            Список запусков процессов с информацией о статусе,
            времени выполнения и возможных ошибках.

    Notes:
        Тип возвращаемых данных определяется полем `mode`.
    """
    return await system.monitoring.determine_type(data.mode)
