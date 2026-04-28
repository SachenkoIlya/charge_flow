from core.logger.logger import make_logger
from etl.utils.with_retry.retry import with_retry
from etl.database.manager import Manager
from core.base_db import Base
from core.storage.client import S3Client
from etl.clients.workspace.workspace import WorkSpase
from etl.runtime.export.DataFramePipeline.df_pipeline import DataFramePipeline
import os


class Settings:
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"


class Ctx:
    def __init__(self, base_db: "Base", type_method: str, run_mode: str, run_id: str, operator: str):
        self.request = with_retry
        self.logger = make_logger(__name__, use_telegram=False)
        
        self.run_mode = run_mode
        self.type_method = type_method
        self.run_id = run_id
        self.operator = operator
        
        
        self.base_db = base_db
        
        self.settings = Settings()
        self.db = Manager(base_db)
        self.s3 = S3Client(self.logger)
        
        self.work_spase = WorkSpase(self)
        self.df_flow = DataFramePipeline(self)





    