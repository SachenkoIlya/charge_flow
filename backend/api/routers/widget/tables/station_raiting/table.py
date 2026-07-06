from datetime import datetime
from backend.api.routers.widget.tables.db import TableDB
from backend.core.date_insurance import date_insurance_from_dict
from backend.core.period_date import _calc_utilisation
from core.base_db import Base


class StationRating:
    def __init__(self, db: "TableDB"):
        self.db = db
    
    async def get_normalize_data(
        self,
        user_id:int,
        params: dict
    ):
        
        date_from, date_to = date_insurance_from_dict(params)

        rows = await self.db.get_station_revenue_stats(
            user_id=user_id, 
            date_from=date_from, 
            date_to=date_to
        )
        
        station = []
        
        for row in rows:
            charging_minutes=float(row['charging_minutes'])
            evse_count=float(row['evse_count'])
            utilisation = _calc_utilisation(
                charging_minutes=charging_minutes,
                evse_count=evse_count,
                date_from=date_from,
                date_to=date_to
            )
            
            station.append({
                "station_id": int(row["station_id"]),
                "station_name": row['station_name'].replace('"', '').replace("'", ''),
                "revenue": round(float(row["total_revenue"]), 2),
                "utilisation": round(utilisation, 2),
            })
        
        stations_sorted = sorted(
            station,
            key=lambda x: x['revenue'], 
            reverse=True
        )
        return {
            "top_stations": stations_sorted[:5],
            "worst_stations": stations_sorted[-5:][::-1],
        }
