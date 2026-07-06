from fastapi import APIRouter, Depends
from backend.api.routers.dashboard.manager import ManagerWidget
from backend.api.routers.widget.tables.schemas import TablesRequestSchema
from backend.dependencies.get_manager import get_current_token, get_widget



ENDPOINT = '/tables'
DESCRIPTION = (
    "Получение данных для аналитических таблиц\n\n"
    "Возвращает структурированные и отсортированные данные (например, рейтинги станций), "
    "предназначенные для отображения в виде табличных отчетов на панели управления (Dashboard)."
)

router = APIRouter(
    prefix='/v1/widget', 
    tags=['widget']
)

@router.post(
    ENDPOINT,
    description=DESCRIPTION,
    response_model_exclude_none=True,
    response_model=''
)
async def tables(
    payload: TablesRequestSchema,
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
    