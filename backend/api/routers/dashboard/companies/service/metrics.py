from backend.api.routers.dashboard.companies.db import UserRepositoryDB
from backend.api.routers.dashboard.stats.db import StatsDB
from core.base_db import Base


class MetricsStats:
    def __init__(self, base_db: "Base"):
        self.stats = StatsDB(base_db)
       



class  UserRepositoryMetrics:
    def __init__(self,  base_db: "Base"):
        self.db = UserRepositoryDB(base_db)

    async def get_companies(self):
        return await self.normalize_company_data()
    
    
    async def normalize_company_data(self):
        rows = await self.db.get_company()
        return [
            {
                'id': r['id'],
                'name': r['company']
            }
            for r in rows
        ]
    
    