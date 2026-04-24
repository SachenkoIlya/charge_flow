from fastapi import FastAPI
from core.base_db import Base
from backend.database.manager import Manager
from fastapi.middleware.cors import  CORSMiddleware
from backend.api.routers.dashboard.manager import ManagerMetrics
from contextlib import asynccontextmanager
import httpx
import os
from dotenv import load_dotenv
from core.logger.logger import make_logger
from backend.api.router import api_router
load_dotenv()

logger = make_logger(__name__, use_telegram=False)
base_url = os.getenv('BASE_URL', 'http://localhost:8000')

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = Base()
    await db.connect()
    
    db_manager = Manager(db)
    app.state.db_manager = db_manager   
    app.state.metrics = ManagerMetrics(db)
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
        base_url
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)