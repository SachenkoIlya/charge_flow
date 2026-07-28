from fastapi import APIRouter, Depends
from backend.api.routers.dashboard.summary.schemas import SummaryResponseModel
from backend.dependencies.get_manager import get_current_token, get_dashboard
from backend.core.date_insurance import date_insurance
from backend.core.schemas import DashboardFilterSchema
from backend.api.routers.dashboard.manager import ManagerDashboardMetrics

ENDPOINT = '/summary'
DESCRIPTION = "Возвращает KPI, график динамики, рейтинг станций и сравнение с предыдущим периодом."
router = APIRouter(prefix='/v1/dashboard', tags=['dashboard'])



@router.post(
    ENDPOINT, 
    summary='Сводка dashboard',
    description=DESCRIPTION,
    response_model=SummaryResponseModel,
    response_model_exclude_none=True
    )
async def get_summary(
    payload: DashboardFilterSchema,
    dash: ManagerDashboardMetrics=Depends(get_dashboard),
    credentials = Depends(get_current_token),
):  
    """
    Возвращает сводную аналитику dashboard за выбранный период.

    Endpoint используется для наполнения основного экрана dashboard:
    KPI-карточек, графика динамики, рейтинга станций и сравнения
    с предыдущим сопоставимым периодом.

    Args:
        payload (DashboardFilterSchema):
            Фильтр dashboard. Содержит выбранный пользователем период
            `date_from` и `date_to`.

        dash (ManagerDashboardMetrics):
            Менеджер dashboard-метрик, получаемый через FastAPI Depends.

        credentials:
            Данные авторизованного пользователя. Используется `user_id`
            из текущего токена.

    Returns:
        SummaryResponseModel:
            Сводный ответ dashboard, содержащий:

            - requested_metrics — метрики за выбранный период;
            - comparable_metrics — метрики за предыдущий сопоставимый период;
            - requested_period — фактические границы выбранного периода;
            - comparable_period — границы периода сравнения.

    Notes:
        - Период сравнения рассчитывается автоматически и имеет ту же
          продолжительность, что и выбранный период.
        - Поля со значением None исключаются из ответа благодаря
          `response_model_exclude_none=True`.
        - Бизнес-логика и расчёт метрик находятся в
          `dash.summary.get_summary_with_comparison()`.
    """
    user_id = credentials.get('user_id')
    # date_from, date_to = date_insurance(payload)
    
    return await dash.summary.get_summary_with_comparison(
        user_id=user_id,
        payload=payload,
    )
    