
from core.base_db import Base
from backend.api.routers.system.db import SystemDb
from backend.api.routers.system.schemas import (
    MonitoringSchema, 
    EtlRunsResponseSchema
)


class SystemReposytory:
    def __init__(self, base_db: "Base"):
        self.db = SystemDb(base_db)

    def get_map_func(self, mode: str):
        MAPPING = {
            'etl_run': self.get_etl_runs,
            'bi_exports': self.get_bi_exports_runs,
        }
        if mode not in MAPPING:
            raise ValueError(f'Unknown mode: {mode}')
        return MAPPING[mode]
    
    @staticmethod
    def normalize_monitoring(rows):
        normaliized =  [
            MonitoringSchema.model_validate(dict(row))
            for row in rows
        ]
        return EtlRunsResponseSchema(rows=normaliized)
    
    async def determine_type(self, mode: str):
        return await self.get_map_func(mode)()

    async def get_etl_runs(self):
        rows = await self.db.get_data_etl_run()
        return self.normalize_monitoring(rows)
    
    async def get_bi_exports_runs(self):
        rows = await self.db.get_data_bi_exports()
        return self.normalize_monitoring(rows)