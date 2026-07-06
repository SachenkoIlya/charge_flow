from fastapi import APIRouter, Depends

from backend.api.routers.dashboard.finance.schemas import FinanceFilterSchema
from backend.dependencies.get_manager import get_current_token, get_dashboard
from backend.api.routers.dashboard.manager import ManagerDashboardMetrics


ENDPOINT = '/finance'
DESCRIPTION = (
    'Возвращает данные финансового дашборда: ключевые показатели '
    '(выручка, EBITDA, чистая прибыль), P&L по станциям, план-факт анализ, '
    'CAPEX, денежный поток, окупаемость, структуру затрат и аналитические графики.'
)

router = APIRouter(prefix='/v1/dashboard', tags=['dashboard'])

@router.post(
    ENDPOINT, 
     summary='Финансовые показатели dashboard',
    description=DESCRIPTION,
    response_model_exclude_none=True,
    response_model='')
async def get_finance(
    payload: FinanceFilterSchema,
    dash: ManagerDashboardMetrics=Depends(get_dashboard),
    credentials=Depends(get_current_token),
):

    """Возвращает финансовые метрики для панели управления (dashboard) пользователя.

    Метод извлекает `user_id` из токена авторизации и запрашивает агрегированные
    финансовые показатели на основе переданного фильтра (toggle-значения).

    Args:
        payload: Схема фильтрации данных (содержит параметр `toggle_value`).
        dash: Менеджер метрик дашборда для работы с бизнес-логикой и расчетами.
        credentials: Данные декодированного JWT-токена авторизованного пользователя.

    Returns:
        Any: Объект или словарь с рассчитанными финансовыми показателями, 
            где все пустые значения (None) будут автоматически исключены.
    """
    user_id = credentials.get('user_id')
    return await dash.finance.get_metrics(user_id, payload.toggle_value)