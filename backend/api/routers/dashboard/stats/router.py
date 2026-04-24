from backend.api.routers.dashboard.manager import ManagerMetrics
from backend.api.routers.dashboard.stats.schemas import DashboardFilterSchema, StatsResponseSchema
from backend.database.get_manager import get_current_token, get_manager, get_merics
from core.logger.logger import make_logger
from backend.database.manager import Manager
from fastapi import APIRouter
from fastapi import Depends
from datetime import datetime, timezone, timedelta


logger = make_logger(__name__, use_telegram=False)

router = APIRouter(prefix='/dashboard', tags=['stats'])

def get_valid_id(role:str, data: DashboardFilterSchema, user_id: int):
    valid_id = None
    if role == 'admin':
        logger.debug(f"role: {role}, используем id: {data.company_id}".upper())
        valid_id = data.company_id
    else:
        logger.debug(f"role: {role}, используем id: {user_id}".upper())
        valid_id = user_id
    return valid_id

def date_insurance(data: DashboardFilterSchema) -> tuple[str, str]:
    today = datetime.now()
    if not data.date_from:
        data.date_from = today.strftime('%d.%m.%Y')

    if not data.date_to:
        data.date_to = data.date_from

    date_from = datetime.strptime(data.date_from, "%d.%m.%Y")
    date_to = datetime.strptime(data.date_to, "%d.%m.%Y") + timedelta(days=1)

    date_from = date_from.replace(tzinfo=timezone.utc)
    date_to = date_to.replace(tzinfo=timezone.utc)
    return date_from, date_to

@router.post('/stats', response_model=StatsResponseSchema)
async def stats(
    data: DashboardFilterSchema, 
    payload = Depends(get_current_token),
    db_manager: Manager=Depends(get_manager),
    metrics:  ManagerMetrics=Depends(get_merics)
):
   
    date_from, date_to = date_insurance(data=data)
    role = payload.get('role')
    user_id = payload.get('user_id')
    valid_id = get_valid_id(
        role=role,
        data=data,
        user_id=user_id
    )
   
  
    result = await metrics.stats.get_metrics(
        valid_id=valid_id,
        date_from=date_from,
        date_to=date_to
    )
    logger.warning(result)
    return result