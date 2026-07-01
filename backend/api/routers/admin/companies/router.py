from backend.dependencies.get_manager import get_merics
from backend.services.admin_required import admin_required
from core.logger.logger import logger
from backend.api.routers.dashboard.manager import ManagerMetrics
from backend.api.routers.admin.companies.schemas import CompanySchema
from fastapi import APIRouter
from fastapi import Depends


router = APIRouter(prefix='/dashboard', tags=['companies'])


@router.get('/companies', response_model=list[CompanySchema])
async def companies(
    _: None = Depends(admin_required),
    metrics:  ManagerMetrics=Depends(get_merics)

):
    
    return await metrics.user_reposytory.get_companies()