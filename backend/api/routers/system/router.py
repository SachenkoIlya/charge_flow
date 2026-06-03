from pydantic import BaseModel

from backend.api.routers.dashboard.manager import ManagerSystem
from backend.api.routers.system.schemas import SystemSchema, EtlRunsResponseSchema
from backend.database.get_manager import get_current_token, get_system
from fastapi import APIRouter
from fastapi import Depends




router = APIRouter(prefix='/system', tags=['system'])



@router.post('/monitoring', response_model=EtlRunsResponseSchema)
async def create(
    data: SystemSchema,
    payload = Depends(get_current_token),
    system:  ManagerSystem=Depends(get_system)
):
    user_id = payload.get('user_id')

    
    return await system.system.determine_type(data.mode)
