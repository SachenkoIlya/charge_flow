from core.base_db import Base

class StationInfoDb:
    def __init__(self, base_db: "Base"):
        self.db = base_db

    async def get_station(self, requested_id:int):
        q = """
            SELECT 
                location_name as label,
                COUNT(*) as stations_count,
                ARRAY_AGG(id ORDER BY key) AS station_ids,
                ARRAY_AGG(key ORDER BY key) AS station_keys
            FROM info_station
            WHERE user_id = $1
            GROUP BY location_name
            ORDER BY location_name;          
            """
        async with self.db.pool.acquire() as conn:
            return await conn.fetch(q, requested_id)
        
