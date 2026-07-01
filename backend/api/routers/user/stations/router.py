from fastapi import APIRouter
from fastapi import Depends
from backend.api.routers.user.stations.schemas import StationSchemas
from backend.api.routers.dashboard.manager import ManagerFinance
from backend.dependencies.get_manager import get_current_token, get_merics_investment


ENDPOINT = '/stations'
router = APIRouter(prefix='/stations', tags=['stations'])


@router.get(ENDPOINT, response_model=list[StationSchemas])
async def station(
    metrics: ManagerFinance=Depends(get_merics_investment),
    payload = Depends(get_current_token),
):
    user_id = payload.get('user_id')
    return await metrics.station_info.get_stations(user_id)