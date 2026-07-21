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
    def build_response(
        result: dict, 
        period:str, 
        date_from:datetime=None, 
        date_to: datetime=None
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
        # Добавляем в ответ информацию о временном фильтре
        # prepare_result['date_range'] = {
        #     'period': period,
        #     'date_from': date_from.strftime("%Y-%m-%d %H:%M:%S") if date_from else None,
        #     'date_to': date_to.strftime("%Y-%m-%d %H:%M:%S") if date_to else None,
        # }
         
        # Извлекаем базовые значения для расчетов
        revenue = prepare_result['metrics'].get('total_revenue', 0)
        investment = prepare_result.get('investment')
         # Суммы берутся из блока инвестиций
        capex = investment.get('capex')
        opex = investment.get('opex')
        
        # считаем без налогов
        opex_amount_for_ebidta = sum(
            float(opex[o]) for o in opex if o != 'taxes'
        )
        opex_total_amount = sum(
            float(opex[o]) for o in opex
        )

        # 1. EBITDA = Выручка минус Операционные расходы. Капитальные вложения (CAPEX) здесь НЕ учитываются.
        # Налоги не учитываются
        ebitda = round(revenue - opex_amount_for_ebidta, 2)
        
        capex_total_amount = sum(
            float(capex[c]) for c in capex 
        )
       
        net_profit = round(revenue - opex_total_amount, 2)
        cash_flow = round(revenue - opex_total_amount - capex_total_amount, 2)
        
        prepare_result['metrics'].update({
            # 'capex': capex,
            # 'opex': opex,
            'ebitda': ebitda,
            'net_profit': net_profit,
            'cash_flow': cash_flow 
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
       
        result = {}
        records = await self.db.get_investment_group(user_id, date_from, date_to)
        for record in records:
            mode = record.get('mode')
            amount_type = record.get('amount_type')
            amount = float(record.get('amount', 0))
            
            if mode not in result:
                result[mode] = {}
            
            result[mode][amount_type] = amount

        return result
    

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