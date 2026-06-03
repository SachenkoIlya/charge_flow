from fastapi import APIRouter
from fastapi import Depends
from backend.api.routers.dashboard.station.schemas import StationSchemas
from backend.api.routers.dashboard.stats.schemas import DashboardFilterSchema
from backend.api.routers.dashboard.manager import ManagerFinance
from backend.database.get_manager import get_current_token, get_merics_investment
from backend.core.valid_id import get_valid_id  
from core.logger.logger import logger


ENDPOINT = '/stations'
router = APIRouter(prefix='/stations', tags=['stations'])


@router.get(ENDPOINT, response_model=list[StationSchemas])
async def station(
    # data: DashboardFilterSchema,
    metrics: ManagerFinance=Depends(get_merics_investment),
    payload = Depends(get_current_token),
):
    
    logger.debug(payload)
    
    user_id = payload.get('user_id')
    return await metrics.station_info.get_stations(user_id)