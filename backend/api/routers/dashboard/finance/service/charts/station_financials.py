from backend.api.routers.dashboard.finance.db import FinanceDB
from backend.api.routers.dashboard.finance.service.conext import PeriodContext
from asyncpg import Record


class StationFinancials:
    def __init__(self, repository : "FinanceDB"):
        self.repository = repository 
        self.chart_name = 'station_financials'

    @staticmethod
    def _normalize_row(row: Record) -> dict:
        revenue = float(row['total_revenue'] or 0)
        electricity_cost = float(
            row['electricity_compensation'] or 0
        )
        operator_commission = float(
            row['operator_commission'] or 0
        )
        taxes = float(row['taxes'] or 0)

        opex = sum([
            operator_commission,
            float(row['rent_payment'] or 0),
            float(row['service_maintenance'] or 0),
            float(row['internet_and_connection'] or 0),
            float(row['insurance'] or 0),
            float(row['other_expenses'] or 0),
        ])

        gross_profit = revenue - electricity_cost
        ebitda = gross_profit - opex
        net_profit = ebitda - taxes

        margin = (
            net_profit / revenue * 100
            if revenue
            else 0
        )

        return {
            'station_id': row['station_id'],
            'station_name': row['location_name'],
            'revenue': round(revenue, 2),
            'electricity_cost': round(electricity_cost, 2),
            'gross_profit': round(gross_profit, 2),
            'opex': round(opex, 2),
            'ebitda': round(ebitda, 2),
            'taxes': round(taxes, 2),
            'net_profit': round(net_profit, 2),
            'net_margin': round(margin, 2),
        }

    async def get_data(
        self, 
        ctx: PeriodContext
    ) -> list[dict]:
        rows = await self.repository.get_station_financials(
            user_id=ctx.user_id,
            date_from=ctx.date_from,
            date_to=ctx.date_to
        )
        return [
            self._normalize_row(row)
            for row in rows
        ]

