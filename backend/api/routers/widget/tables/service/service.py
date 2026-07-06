

from backend.api.routers.widget.tables.db import TableDB
from backend.api.routers.widget.tables.schemas import TablesRequestSchema
from backend.api.routers.widget.tables.service.register_table import REGISTER_TABLE
from core.base_db import Base
import asyncio

class TableService:
    def __init__(self, base_db: "Base"):
        self.db = TableDB(base_db)

    async def get_data(
        self, 
        user_id:int,
        payload:TablesRequestSchema, 
    ):
        tasks = []
        
        for name, params in payload.model_dump(exclude_none=True).items():
            handler_cls = REGISTER_TABLE.get(name, None)

            if handler is None:
                continue
            
            handler = handler_cls(self.db)
            tasks.append(
                handler.get_normalize_data(
                    user_id, 
                    params, 
                )
            )
        
        if not tasks:
            return 
        result = await asyncio.gather(*tasks, return_exceptions=True)