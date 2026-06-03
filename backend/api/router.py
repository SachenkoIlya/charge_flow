from fastapi import APIRouter

from backend.api.routers.auth.login import router as login_router
from backend.api.routers.auth.auth import router as auth_router
from backend.api.routers.auth.connect_operator import router as router_operator
from backend.api.routers.dashboard.stats.router import router as stats_router
from backend.api.routers.dashboard.companies.router import router as companies_router
from backend.api.routers.dashboard.station.router import  router as station_router
from backend.api.routers.investments.investments_and_expenses.router import router as investments_router
api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(login_router)
api_router.include_router(router_operator)
api_router.include_router(stats_router)
api_router.include_router(companies_router)
api_router.include_router(station_router)
api_router.include_router(investments_router)
