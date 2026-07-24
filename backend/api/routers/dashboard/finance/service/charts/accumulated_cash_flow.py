

from backend.api.routers.dashboard.finance.db import FinanceDB
from datetime import datetime   
from asyncpg import Record
from backend.api.routers.dashboard.finance.service.conext import PeriodContext
from core.logger.logger import logger

class CashFlowHistory:
    def __init__(self,  db: "FinanceDB"):
        self.repository = db
        self.chart_name = 'cash_flow_history'

    @staticmethod
    def _normalize_group_cost_structure_records(rows: list[Record]) -> dict:
        """Преобразовать записи БД в словарь с текстовыми датами и суммами в формате float."""
        return {
            r['month_date'].strftime("%Y-%m-%d"): float(r['opex_expenses'])
            for r in rows
        }

    @staticmethod
    def _normalize_group_month_revenue(rows: list[Record]) -> dict:
        return {
            r['month_date'].strftime("%Y-%m-%d"): {
                'total_revenue': float(r['total_revenue']),
                'owner_revenue': float(r['owner_revenue']),
                'operator_commission': float(r['operator_commission']),
            }
            for r in rows
        }
    
    async def get_group_month_cost_structure(
        self,
        user_id:int,
    ) -> dict:
        """Получить агрегированные по месяцам финансовые операции из БД без фильтрации по датам."""
        rows = await self.repository.get_group_month_cost_structure(
            user_id=user_id,
        )
        return self._normalize_group_cost_structure_records(rows)


    async def get_group_month_revenue(
        self, 
        user_id: int
    ) -> dict:
        rows = await self.repository.get_group_month_revenue(user_id)
        return self._normalize_group_month_revenue(rows)
    
    async def get_data(
        self, 
        ctx: PeriodContext
        ) -> dict:
        """Получить финальные нормализованные данные для построения графика накопленного потока."""
        accumulated = 0
        result = []

        opex_data = await self.get_group_month_cost_structure(
            user_id=ctx.user_id,
        )
        revenue_data = await self.get_group_month_revenue(ctx.user_id)
        for month, revenue in revenue_data.items():
            opex = opex_data.get(month, 0)

            net_cash_flow = revenue['owner_revenue'] - opex
            accumulated += net_cash_flow 
            res = {
                'date': month,
                'accumulated': accumulated,
                'net_cash_flow': net_cash_flow
            }
            result.append(res)

        return  result