from backend.api.routers.dashboard.finance.db import FinanceDB
from core.base_db import Base
from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta
from backend.core.gather_named import gather_named
from backend.core.period_date import get_date_range_from_period
from core.logger.logger import logger



class MetricFinance:
    def __init__(self, base_db: "Base"):
        self.db = FinanceDB(base_db)

    async def get_normalize_metrics(self, user_id:int, date_from: datetime=None, date_to:datetime=None):
        rows = await self.db.get_metrics(user_id, date_to, date_from)
        return {
            'total_revenue': round(float(rows['total_revenue']), 2)
        }
    
    async def get_normalize_investment_metrics(
        self, 
        user_id: int, 
        date_from: datetime=None, 
        date_to:datetime=None,
        mode:str='opex', 
    ):
        rows = await self.db.get_investment(
            user_id=user_id,
            date_from=date_from,
            date_to=date_to,
            mode=mode
        )
        total_investemn = sum(r['amount'] for r in rows)
        return int(total_investemn)
    
    async def get_metrics(self, user_id: int, period: str):
        date_from, date_to = get_date_range_from_period(period)
       
        data = {
            'metrics': self.get_normalize_metrics(
                user_id=user_id,
                date_from=date_from,
                date_to=date_to
            ),
            'opex': self.get_normalize_investment_metrics(
                user_id=user_id,
                date_from=date_from,
                date_to=date_to,
            ),
            'capex': self.get_normalize_investment_metrics(
                user_id=user_id,
                date_from=date_from,
                date_to=date_to,
                mode='capex'
            )
        }

        result = await gather_named(data)
        result['date_range'] = {
            'period': period,
            'date_from': date_from.strftime("%Y-%m-%d %H:%M:%S") if date_from else None,
            'date_to': date_to.strftime("%Y-%m-%d %H:%M:%S") if date_to else None,
        }
        logger.debug(result)
        revenue = result['metrics'].get('total_revenue', 0)
        opex = result.pop('opex', 0)
        capex = result.pop('capex', 0)

        result['metrics'].update({
            'opex': opex,
            'capex': capex,
            'ebitda': round(revenue - opex, 2),
            'net_profit': round(revenue - opex, 2),
            'cash_flow': round(revenue - opex - capex, 2)
        })
        return result