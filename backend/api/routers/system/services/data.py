
from core.base_db import Base
from backend.api.routers.system.db import SystemDb
from backend.api.routers.system.schemas import EtlRunSchema, EtlRunsResponseSchema
class SystemReposytory:
    def __init__(self, base_db: "Base"):
        self.db = SystemDb(base_db)

    @staticmethod
    def normalize_etl_run(rows):
        normaliized =  [
            EtlRunSchema.model_validate(dict(row))
            for row in rows
        ]
        return EtlRunsResponseSchema(rows=normaliized)
    
    
    async def determine_type(self, mode: str):
        if mode == 'etl_run':
            await self.get_etl_runs()


    async def get_etl_runs(self):
        rows = await self.db.get_data_etl_run()
        return self.normalize_etl_run(rows)