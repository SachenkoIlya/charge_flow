from fastapi import APIRouter
from fastapi import Depends
from backend.api.routers.user.stations.schemas import StationSchemas
from backend.api.routers.dashboard.manager import ManagerFinance
from backend.dependencies.get_manager import get_current_token, get_merics_investment


ENDPOINT = '/stations'
description = """
Получение списка доступных станций

Возвращает массив всех станций, к которым текущий пользователь имеет доступ.
Данные используются для отображения списка объектов и заполнения выпадающих списков на фронтенде.
"""
router = APIRouter(
    prefix='/v1/stations', 
    tags=['stations']
)


@router.get(
    ENDPOINT, 
    description=description,
    response_model=list[StationSchemas]
    )
async def station(
    metrics: ManagerFinance=Depends(get_merics_investment),
    payload = Depends(get_current_token),
):
    """Возвращает список станций, привязанных к текущему пользователю.

    Метод извлекает `user_id` из токена авторизации и запрашивает через 
    сервис финансовых метрик список станций, к которым у пользователя есть права.

    Args:
        metrics: Менеджер финансовых метрик для работы с бизнес-логикой и БД.
        payload: Данные декодированного JWT-токена авторизованного пользователя.

    Returns:
        list[StationSchemas]: Список объектов станций с их параметрами.
    """
    user_id = payload.get('user_id')
    return await metrics.station_info.get_stations(user_id)