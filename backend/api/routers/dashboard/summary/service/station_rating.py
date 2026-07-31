

from backend.api.routers.dashboard.finance.service.conext import PeriodContext
from backend.api.routers.dashboard.summary.db import SummaryDB
from backend.utils.calc_utilisation import _calc_utilisation



class StationRating:
    def __init__(self, repository: "SummaryDB"):
        self.repository = repository

    async def get_station_rating(
        self,
        ctx: PeriodContext
    ):
        rows = await self.repository.get_station_revenue_stats(
            user_id=ctx.user_id, 
            date_from=ctx.date_from, 
            date_to=ctx.date_to,
        )
            
        station = []
        for row in rows:
            charging_minutes=float(row['charging_minutes'])
            evse_count=float(row['evse_count'])
            utilisation = _calc_utilisation(
                charging_minutes=charging_minutes,
                evse_count=evse_count,
                date_from=ctx.date_from,
                date_to=ctx.date_to
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