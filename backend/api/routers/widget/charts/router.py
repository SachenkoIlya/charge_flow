from fastapi import APIRouter, Depends
from backend.api.routers.dashboard.manager import ManagerWidget
from backend.api.routers.widget.charts.schemas import ChartsRequestSchema
from backend.api.routers.widget.charts.service.service import ChartService
from backend.dependencies.get_manager import get_current_token, get_widget
from core.logger.logger import logger


ENDPOINT = '/charts'
DESCRIPTION = (
    "Получение данных для графиков и чартов\n\n"
    "Возвращает агрегированные временные ряды и метрики, специально отформатированные "
    "для визуализации на графиках панели управления (Dashboard)."
)
router = APIRouter(
    prefix='/v1/widget', 
    tags=['widget']
)

@router.post(
    ENDPOINT,
    description=DESCRIPTION,
    response_model_exclude_none=True,
    # response_model=''
)
async def charts(
    payload: ChartsRequestSchema,
    widget: ManagerWidget=Depends(get_widget),
    credentials=Depends(get_current_token),
):
    """
    Формирует наборы данных (datasets) для построения бизнес-графиков.

    Метод авторизует пользователя через токен, извлекает его `user_id` 
    и запрашивает у бизнес-логики дашборда метрики, разбитые по временным точкам 
    в соответствии с выбранным фильтром.
    """
    user_id = credentials.get('user_id')
    logger.debug(f"Deploy +")
    logger.debug(f"user_id: {user_id}")
    # result = 
    logger.debug(payload)
    return {
        'status': "success",
        'user_id': user_id,
        'msg': 'Подключение прошло успешно',
    }