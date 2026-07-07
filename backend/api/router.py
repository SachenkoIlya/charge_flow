from fastapi import APIRouter


from backend.api.routers.auth.login.router import router as login_router
from backend.api.routers.auth.register.router import router as register_router
from backend.api.routers.auth.connect_operator.router import router as router_operator

from backend.api.routers.dashboard.stats.router import router as stats_router
from backend.api.routers.admin.companies.router import router as companies_router
from backend.api.routers.user.stations.router import  router as station_router
from backend.api.routers.investments.investments_and_expenses.router import router as investments_router
from backend.api.routers.admin.system.router import router as system_router
from backend.api.routers.dashboard.summary.router import router as summary_router
from backend.api.routers.dashboard.finance.router import router as finance_router
from backend.api.routers.widget.charts.router import router as charts_router
api_router = APIRouter()

api_router.include_router(register_router)
api_router.include_router(login_router)
api_router.include_router(router_operator)
api_router.include_router(stats_router)
api_router.include_router(companies_router)
api_router.include_router(station_router)
api_router.include_router(investments_router)
api_router.include_router(system_router)
api_router.include_router(summary_router)
api_router.include_router(finance_router)
api_router.include_router(charts_router)
