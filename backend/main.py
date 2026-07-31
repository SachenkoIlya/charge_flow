from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.router import api_router
from backend.manager.dashboard import ManagerDashboardMetrics
from backend.manager.finance import ManagerFinance
from backend.manager.metrics import ManagerMetrics
from backend.manager.system import ManagerSystem
from backend.manager.user import UserAuthManager
from backend.manager.widget import ManagerWidget
from core.base_db import Base
from core.logger.logger import logger
from core.security.settings import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = Base()
    await db.connect()
    
    app.state.metrics = ManagerMetrics(db)
    app.state.investment = ManagerFinance(db)
    app.state.system  = ManagerSystem(db)
    app.state.dashboard = ManagerDashboardMetrics(db)
    app.state.auth = UserAuthManager(db)
    app.state.widget = ManagerWidget(db)
    try:
        app.state.client = httpx.AsyncClient(base_url="http://localhost:8001")
        logger.info(f"client created".upper())
        yield
        await app.state.client.aclose()
        logger.info(f"client closed".upper())
    finally:
        await db.close()

app = FastAPI(
    lifespan=lifespan, 
    # root_path="/api"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",  
        "http://127.0.0.1:8080",
        settings.BACKEND_URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)