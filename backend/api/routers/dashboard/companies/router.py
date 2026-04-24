from backend.database.get_manager import get_manager, get_merics
from backend.services.admin_required import admin_required
from core.logger.logger import make_logger
from backend.api.routers.dashboard.manager import ManagerMetrics
from backend.api.routers.dashboard.companies.schemas import CompanySchema
from backend.database.manager import Manager
from fastapi import APIRouter
from fastapi import Depends


logger = make_logger(__name__, use_telegram=False)
router = APIRouter(prefix='/dashboard', tags=['companies'])


@router.get('/companies', response_model=list[CompanySchema])
async def companies(
    _: None = Depends(admin_required),
    db_manager: Manager=Depends(get_manager),
    metrics:  ManagerMetrics=Depends(get_merics)

):
    
    return await metrics.user_reposytory.get_companies()