from fastapi import APIRouter
from fastapi import Depends
from backend.api.routers.dashboard.station.schemas import StationSchemas
from backend.api.routers.dashboard.stats.schemas import DashboardFilterSchema
from backend.api.routers.dashboard.manager import ManagerMetrics
from backend.database.get_manager import get_current_token, get_merics
from backend.core.valid_id import get_valid_id  
from core.logger.logger import logger


ENDPOINT = '/station'
router = APIRouter(prefix='/stations', tags=['station'])


@router.get(ENDPOINT, response_model=list[StationSchemas])
async def station(
    data: DashboardFilterSchema,
    metrics: ManagerMetrics=Depends(get_merics),
    payload = Depends(get_current_token),
):
    
    logger.debug(data)
    logger.debug(payload)
    
    user_id = payload.get('user_id')
    
    return await metrics.station_info.get_stations(user_id)