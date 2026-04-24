


import asyncio

from backend.api.routers.dashboard.stats.db import StatsDB
from core.base_db import Base


class MetricStats:
    def __init__(self, base_db: "Base"):
        self.db = StatsDB(base_db)
       
    @staticmethod
    def empty_metrics():
        return {
            "total_revenue": 0,
            "my_revenue": 0,
            "operator_revenue": 0,
            "operator_percent": 0,
            "total_energy_kwh": 0,
            "average_bill": 0,
            "total_users": 0,
            "avg_charge_time": 0,
            "success_sessions": 0,
            "total_sessions": 0,
        }
    
    async def normalize_metrics_total_staion(self, valid_id):
        row = await self.db.get_total_station(valid_id)
        return  row['total_station']
    
    async def normalize_metrics(self, valid_id, date_from, date_to):
        row = await self.db.get_metrics(
                user_id=valid_id,
                date_from=date_from,
                date_to=date_to
            )
        return {
            "total_revenue": float(row['total_revenue']),
            "my_revenue": float(row['my_revenue']),
            "operator_revenue": float(row['operator_revenue']),
            "operator_percent": float(row['operator_percent']),
            "total_energy_kwh": float(row['total_energy_kwh'] or 0),

            "average_bill": float(row['average_bill']),
            "total_users": int(row['total_users']),
            "avg_charge_time": float(row['avg_charge_time']),

            "success_sessions": int(row['success_sessions']),
            "total_sessions": int(row['total_sessions']),
        }
    
    async def normalize_metrics_chart(self, valid_id, date_from, date_to):
        rows = await self.db.get_data_chart(
                user_id=valid_id,
                date_from=date_from,
                date_to=date_to
        )
        return [
            {
                'value': int(r['value']),
                'name': r['name'],
                
            }
            for r in rows
        ]

    async def get_metrics(self, valid_id, date_from, date_to):
        data = {}
        is_fallback = False

        tasks = {
            'metrics': self.normalize_metrics(valid_id, date_from, date_to),
            'chart': self.normalize_metrics_chart(valid_id, date_from, date_to),
            'total_station': self.normalize_metrics_total_staion(valid_id)
        }
        names = list(tasks.keys())
        tasks = list(tasks.values())
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for name, res in dict(zip(names, results)).items():
            if isinstance(res, Exception):
                is_fallback = True
                data[name] = [] if name == 'chart' else None
            else:
                data[name] = res

        if is_fallback:
            data['metrics'] = data['metrics'] or self.empty_metrics()
            data['chart'] = data['chart'] or []
            data['total_station'] = data['total_station'] or 0
        data['meta'] = {"is_fallback": is_fallback}
        return data