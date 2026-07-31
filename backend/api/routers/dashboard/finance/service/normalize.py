from backend.api.routers.dashboard.finance.db import FinanceDB
from backend.api.routers.dashboard.finance.service.conext import PeriodContext
from datetime import datetime


class FinanceMetricsService:
    """
    Сервис получения и подготовки финансовых метрик.

    Отвечает за работу с финансовыми данными пользователя:
    получает агрегированные значения из слоя БД, считает производные
    показатели и формирует итоговую структуру ответа для API/UI.

    Основные задачи:
    - получить выручку пользователя за период;
    - получить сумму инвестиций/расходов по типу операции;
    - рассчитать OPEX, CAPEX, EBITDA, чистую прибыль и cash flow;
    - добавить в ответ информацию о выбранном периоде.

    Attributes:
        db (FinanceDB):
            Объект доступа к финансовым данным.
    """
    def __init__(self, repository: "FinanceDB"):
        self.repository = repository
        
    @staticmethod
    def calculate_payback_period(
        net_profit:float, 
        capex_total_amount:float,
        date_from:datetime,
        date_to:datetime
    ) ->float:
        payback_period = None

        if (
            net_profit > 0
            and capex_total_amount > 0
            and date_from is not None
            and date_to is not None
        ):
            months_count = (date_to.year - date_from.year) * 12
            months_count += date_to.month - date_from.month
            months_count += (date_to.day - date_from.day) / 30.4

            months_count = max(months_count, 1.0)

            monthly_net_profit = net_profit / months_count

            if monthly_net_profit > 0:
                payback_period = round(
                    capex_total_amount / monthly_net_profit,
                    1,
                )

        return payback_period
    

    @staticmethod
    def calculate_financial_indicators(prepare_result:dict) -> dict:
        # Извлекаем базовые значения для расчетов
        revenue = prepare_result['metrics'].get('total_revenue', 0)
        investment = prepare_result.get('investment')
         # Суммы берутся из блока инвестиций
        capex = investment.get('capex')
        opex = investment.get('opex')
        # считаем без налогов
        opex_amount_for_ebidta = 0
        opex_total_amount = 0
        capex_total_amount = 0

        if opex:
            opex_amount_for_ebidta = sum(
                float(opex[o]) for o in opex if o != 'taxes'
            ) 
            opex_total_amount = sum(
                float(opex[o]) for o in opex
            ) 
        if capex:
            capex_total_amount = sum(
                float(capex[c]) for c in capex 
            )
        # 1. EBITDA = Выручка минус Операционные расходы. Капитальные вложения (CAPEX) здесь НЕ учитываются.
        # Налоги не учитываются
        ebitda = round(revenue - opex_amount_for_ebidta, 2)
        net_profit = round(revenue - opex_total_amount, 2)
        cash_flow = round(revenue - opex_total_amount - capex_total_amount, 2)
        return {
            'ebitda': ebitda,
            'net_profit': net_profit,
            'cash_flow': cash_flow
        }, capex_total_amount
    
    async def get_metrics(
        self, 
        ctx: PeriodContext
    ) -> dict[str, float]:
        """
        Получить основные финансовые метрики пользователя за период.

        Args:
            user_id (int):
                Идентификатор пользователя.

            date_from (datetime | None):
                Начальная дата периода.

            date_to (datetime | None):
                Конечная дата периода.

        Returns:
            dict[str, float]:
                Словарь с общей выручкой пользователя.
        """
        rows = await self.repository.get_metrics(
            ctx.user_id, 
            ctx.date_from, 
            ctx.date_to,
            ctx.station_ids
        )
        return {
            'total_revenue': round(float(rows['total_revenue']), 2)
        }
    
    async def get_investment_metrics(
        self, 
        ctx: PeriodContext
    ) -> dict[str, float | int]:
       
        investment = {
            "capex": {
                "construction_and_installation": 0,
                "other_capex": 0,
                "location_search": 0,
                "equipment_purchase": 0
                },
            "opex": {
                "insurance": 0,
                "taxes": 0,
                "service_maintenance": 0,
                "internet_and_connection": 0,
                "rent_payment": 0,
                "other_expenses": 0,
                "electricity_compensation": 0
            }
        }
        records = await self.repository.get_investment_group(
            user_id=ctx.user_id, 
            date_from=ctx.date_from, 
            date_to=ctx.date_to,
            station_ids=ctx.station_ids
        )
        
        for record in records:
            mode = record.get('mode')
            amount_type = record.get('amount_type')
            amount = float(record.get('amount', 0))
            if mode in investment:
                investment[mode][amount_type] = amount
        return investment
    

    async def get_date_range(
        self, 
        ctx:PeriodContext,
        mask = "%Y-%m-%d %H:%M:%S"
    ):
        date_from = ctx.date_from
        date_to = ctx.date_to

        if date_from is None and date_to is None:
            rows = await self.repository.get_date_range(
                user_id=ctx.user_id,
            ) 
            date_from = rows['first_date']
            date_to = rows['last_date']

        date_from = date_from.strftime(mask) if date_from else None
        date_to = date_to.strftime(mask) if date_to else None
        
        return {
            'period': ctx.period,
            'date_from': date_from,
            'date_to': date_to,
        }