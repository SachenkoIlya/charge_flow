from backend.dependencies.get_manager import get_merics
from backend.dependencies.admin_required import admin_required
from backend.manager.metrics import ManagerMetrics
from backend.api.routers.admin.companies.schemas import CompanySchema
from fastapi import APIRouter
from fastapi import Depends


ENDPOINT = '/companies'
description = (
    "Получает список всех компаний, принадлежащих пользователям с ролью 'investor'. "
    "Возвращает массив объектов с идентификаторами и названиями компаний."
)

router = APIRouter(
    prefix='/dashboard', 
    tags=['companies']
)


@router.get(
    ENDPOINT,
    description=description,
    response_model=list[CompanySchema]
)
async def companies(
    _: None = Depends(admin_required),
    metrics:  ManagerMetrics=Depends(get_merics)

):
    """Возвращает список компаний инвесторов для панели управления.

    Args:
        _: Проверка прав администратора (выбрасывает HTTP 403 при отсутствии доступа).
        metrics: Менеджер метрик и репозиториев для работы с данными.

    Returns:
        list[CompanySchema]: Список объектов компаний с их ID.
    """
    return await metrics.user_reposytory.get_companies()