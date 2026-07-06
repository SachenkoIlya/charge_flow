from fastapi import FastAPI
from backend.api.routers.auth.manager import UserAuthManager
from core.base_db import Base
from backend.services.manager import Manager
from fastapi.middleware.cors import  CORSMiddleware

from backend.api.routers.dashboard.manager import (
    ManagerMetrics, 
    ManagerFinance, 
    ManagerSystem,
    ManagerDashboardMetrics,
    ManagerWidget
)

from core.security.settings import settings
from contextlib import asynccontextmanager
import httpx
from core.logger.logger import logger
from backend.api.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = Base()
    await db.connect()
    
    db_manager = Manager(db)
    app.state.db_manager = db_manager   
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

app = FastAPI(lifespan=lifespan)

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