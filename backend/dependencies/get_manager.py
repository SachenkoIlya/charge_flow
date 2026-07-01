from fastapi import Request
from backend.api.routers.auth.manager import UserAuthManager
from backend.api.routers.dashboard.manager import (
    ManagerMetrics, 
    ManagerFinance, 
    ManagerSystem,
    ManagerDashboardMetrics
)

from backend.services.manager import Manager
from typing import cast
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.security.security import security


security_http = HTTPBearer()


def get_current_token(
    credentials: HTTPAuthorizationCredentials = Depends(security_http) 
):
    data_credentials = credentials.credentials
    r = security.decode_token(data_credentials)
    return r


def get_manager(request: Request) -> Manager:
    """
    Получение менеджера базы данных из состояния приложения.

    Используется как dependency (Depends) в FastAPI для доступа к базе данных
    в обработчиках запросов.
    """
    return cast(Manager, request.app.state.db_manager)

def get_user_create(request: Request) -> UserAuthManager:
    return cast(UserAuthManager, request.app.state.auth)

def get_merics(request: Request) -> ManagerMetrics:
    return cast(ManagerMetrics, request.app.state.metrics)

def get_dashboard(request: Request) -> ManagerDashboardMetrics:
    return cast(ManagerDashboardMetrics, request.app.state.dashboard)


def get_merics_investment(request: Request) -> ManagerFinance:
    return cast(ManagerFinance, request.app.state.investment)


def get_system(request: Request) -> ManagerSystem:
    return cast(ManagerSystem, request.app.state.system)