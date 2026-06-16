from fastapi import APIRouter, Depends

from backend.api.routers.dashboard.finance.schemas import FinanceFilterSchema
from backend.dependencies.get_manager import get_current_token, get_dashboard
from backend.api.routers.dashboard.manager import ManagerDashboardMetrics

from core.logger.logger import logger

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

    
    user_id = credentials.get('user_id')
    return await dash.finance.get_metrics(user_id, payload.toggle_value)