from backend.api.routers.dashboard.manager import ManagerMetrics
from backend.api.routers.dashboard.stats.schemas import StatsResponseSchema
from backend.dependencies.get_manager import get_current_token, get_merics
from backend.core.schemas import DashboardFilterSchema
from backend.core.valid_id import get_valid_id  
from backend.core.date_insurance import date_insurance
from core.logger.logger import logger
from fastapi import APIRouter
from fastapi import Depends




router = APIRouter(prefix='/dashboard', tags=['stats'])




@router.post('/stats', response_model=StatsResponseSchema)
async def stats(
    data: DashboardFilterSchema, 
    payload = Depends(get_current_token),
    metrics:  ManagerMetrics=Depends(get_merics)
):
   
    date_from, date_to = date_insurance(data=data)
    role = payload.get('role')
    user_id = payload.get('user_id')
    requested_id = get_valid_id(
        role=role,
        data=data,
        user_id=user_id
    )
   
  
    result = await metrics.stats.get_metrics(
        valid_id=requested_id,
        date_from=date_from,
        date_to=date_to
    )
    logger.warning(result)
    return result