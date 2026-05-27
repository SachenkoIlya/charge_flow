from core.base_db import Base
from backend.api.routers.dashboard.station.db import StationInfoDb


class StationInfo:
    def __init__(self, base_db: "Base"):
        self.db = StationInfoDb(base_db)


    async def get_stations(self, requested_id: int):
        return await self.normalize_data(requested_id)

        

    async def normalize_data(self, requested_id: int) -> list[dict]:
        res = await self.db.get_station(requested_id)

        return [
            {
                'label': r['label'],
                'stations_count': r['stations_count'],
                'station_ids': r['station_ids'],
                'station_keys': r['station_keys']
            
            }
            for r in res
        ]