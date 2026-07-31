

from backend.api.routers.dashboard.finance.service.conext import PeriodContext
from backend.api.routers.dashboard.summary.db import SummaryDB
from asyncpg import Record

class Margin:
    def __init__(self, repository: "SummaryDB"):
            self.repository = repository

    @staticmethod
    def calculate_revenue_split(rows: Record) -> dict[str, float | float]:
        total_revenue = float(rows["total_revenue"])
        station_owner_revenue = float(rows["station_owner_revenue"])
        operator_revenue = float(rows["operator_revenue"])
        total_opex = float(rows["total_opex"])
        net_profit = float(rows["net_profit"])
        
        # Доля партнёра от общей выручки.
        # Показывает, какая часть денег клиентов уходит владельцам ЭЗС.
        partner_share_pct = (
            station_owner_revenue / total_revenue * 100
            if total_revenue > 0
            else 0
        )
        # Доля оператора-агрегатора от общей выручки.
        # Показывает комиссию/доход оператора относительно всей выручки.
        operator_share_pct = (
            operator_revenue / total_revenue * 100
            if total_revenue > 0
            else 0
        )
        # Операционная маржа после OPEX.
        # Показывает, сколько прибыли остается у оператора после расходов.
        net_margin_pct = (
            net_profit / station_owner_revenue * 100
                if station_owner_revenue > 0
                else 0
            )
        return {
            # 'total_revenue': round(total_revenue, 2),
            'station_owner_revenue': round(station_owner_revenue, 2),
            'station_owner_pct': round(partner_share_pct, 2),
            'operator_revenue': round(operator_revenue, 2),
            'operator_commission_pct': round(operator_share_pct, 2),
            'total_opex': round(total_opex, 2),
            'net_profit': round(net_profit, 2),
            'net_margin_pct': round(net_margin_pct, 2),
        }
    
    async def get_margin_pct(
        self,  
        ctx: PeriodContext
    ) -> dict[str, float | float]:
        """
        Рассчитывает распределение выручки между партнёром и оператором
        за указанный период.
        На основании агрегированных финансовых показателей вычисляет:
        - доход партнёра (`partner_revenue`);
        - долю дохода партнёра в общей выручке (`partner_pct`);
        - доход оператора (валовую маржу, `operator_revenue`);
        - долю дохода оператора в общей выручке (`operator_pct`).
        Процентные значения рассчитываются относительно общей выручки.
        Если общая выручка отсутствует или равна нулю, проценты принимают
        значение `0`.
        
        Args:
            user_id (int): Идентификатор пользователя.
            date_from (datetime): Начало периода расчёта.
            date_to (datetime): Конец периода расчёта.

        Returns:
            dict:
                Словарь с финансовыми показателями:
                - partner_revenue (float) — доход партнёра;
                - partner_pct (float) — доля дохода партнёра в общей выручке, %;
                - operator_revenue (float) — доход оператора (валовая маржа);
                - operator_pct (float) — доля дохода оператора в общей выручке, %.
                Все значения округляются до двух знаков после запятой.
        
        Example:
            Возвращаемое значение:
            {
                "partner_revenue": 7500.00,
                "partner_pct": 75.0,
                "operator_revenue": 2500.00,
                "operator_pct": 25.0
            }
        """
        
        rows = await self.repository.get_margin_metrics(
            user_id=ctx.user_id, 
            date_from=ctx.date_from, 
            date_to=ctx.date_to,
            station_ids=ctx.station_ids
        )
        return self.calculate_revenue_split(rows)
    