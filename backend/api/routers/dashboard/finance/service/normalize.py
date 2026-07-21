from backend.api.routers.dashboard.finance.db import FinanceDB
from core.base_db import Base
from datetime import datetime
from core.logger.logger import logger
from copy import deepcopy

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
    def __init__(self, base_db: "Base"):
        self.db = FinanceDB(base_db)
    @staticmethod
    def calculate_payback_period(
        net_profit:float, 
        capex_total_amount:float,
        date_from:datetime,
        date_to:datetime
    ) ->float:
        payback_period = 0
        if (
            net_profit > 0 
            and capex_total_amount > 0 
            and date_from and date_to
        ):
            # Находим точное количество месяцев в выбранном диапазоне дат
            months_count = (date_to.year - date_from.year) * 12 + (date_to.month - date_from.month)
            months_count += (date_to.day - date_from.day) / 30.4
            months_count = max(months_count, 1.0) # Защита от деления на 0
            # Среднемесячная чистая прибыль за этот период
            monthly_net_profit = net_profit / months_count
            # Окупаемость = Весь CAPEX делим на среднюю прибыль в месяц
            payback_period = round(capex_total_amount / monthly_net_profit, 1)
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
    
    def build_response(
        self,
        result: dict, 
        mask:str="%Y-%m-%d %H:%M:%S"
    ) -> dict:
        """
        Сформировать итоговый ответ с финансовыми метриками.

        Метод принимает результат параллельного выполнения запросов,
        добавляет информацию о периоде и рассчитывает производные показатели:
        OPEX, CAPEX, EBITDA, чистую прибыль и денежный поток.

        Args:
            result (dict):
                Словарь с исходными данными:
                - metrics: основные метрики;
                - opex: операционные расходы;
                - capex: капитальные расходы.

            period (str):
                Название выбранного периода.

            date_from (datetime | None):
                Начальная дата периода.

            date_to (datetime | None):
                Конечная дата периода.

        Returns:
            dict:
                Подготовленный ответ с финансовыми метриками и диапазоном дат.
        """
        
        # Создаем глубокую копию
        prepare_result = deepcopy(result)
        date_range = prepare_result.get('date_range')
        
        date_from = date_range.get('date_from')
        date_to = date_range.get('date_to')
        
        date_from = datetime.strptime(date_from, mask)
        date_to = datetime.strptime(date_to, mask)
        
       
        financial_indicators, capex_total_amount = self.calculate_financial_indicators(prepare_result)
        payback_period = self.calculate_payback_period(
            net_profit=financial_indicators.get('net_profit'),
            capex_total_amount=capex_total_amount,
            date_from=date_from,
            date_to=date_to
        )

        prepare_result['metrics'].update({
            **financial_indicators,
            'payback_period': payback_period
            # # 'capex': capex,
            # # 'opex': opex,
            # 'ebitda': ebitda,
            # 'net_profit': net_profit,
            # 'cash_flow': cash_flow 
        })
        return prepare_result
    
    async def get_metrics(
        self, 
        user_id:int, 
        date_from: datetime=None, 
        date_to:datetime=None
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
        rows = await self.db.get_metrics(user_id, date_from, date_to)
        return {
            'total_revenue': round(float(rows['total_revenue']), 2)
        }
    
    async def get_investment_metrics(
        self, 
        user_id: int, 
        date_from: datetime=None, 
        date_to:datetime=None,
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
        records = await self.db.get_investment_group(user_id, date_from, date_to)
        for record in records:
            mode = record.get('mode')
            amount_type = record.get('amount_type')
            amount = float(record.get('amount', 0))
            if mode in investment:
                investment[mode][amount_type] = amount
        return investment
    

    async def get_date_range(
        self, 
        user_id:int,
        period:str,
        date_from: datetime=None,
        date_to: datetime=None,
        mask = "%Y-%m-%d %H:%M:%S"
    ):
        if date_from is None and date_to is None:
            rows = await self.db.get_date_range(
                user_id=user_id,
            ) 
            date_from = rows['first_date']
            date_to = rows['last_date']

        date_from = date_from.strftime(mask) if date_from else None
        date_to = date_to.strftime(mask) if date_to else None
        
        return {
            'period': period,
            'date_from': date_from,
            'date_to': date_to,
        }