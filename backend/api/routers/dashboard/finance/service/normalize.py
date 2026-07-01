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
        prepare_result = deepcopy(result)
        prepare_result['date_range'] = {
            'period': period,
            'date_from': date_from.strftime("%Y-%m-%d %H:%M:%S") if date_from else None,
            'date_to': date_to.strftime("%Y-%m-%d %H:%M:%S") if date_to else None,
        }
       
        revenue = prepare_result['metrics'].get('total_revenue', 0)
        investment = prepare_result.get('investment')

        capex_total_amount = (
            investment.get('capex', {}).get('total_amount', 0)
        )

        opex_total_amount = (
            investment.get('capex', {}).get('total_amount', 0)
        )

        ebitda = round(revenue - opex_total_amount, 2)
        net_profit = round(revenue - opex_total_amount, 2)
        cash_flow = round(revenue - opex_total_amount - capex_total_amount, 2)
        
        prepare_result['metrics'].update({
            # **investment,
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
    
    async def get_investment_metrics_v2(
        self, 
        user_id: int, 
        date_from: datetime=None, 
        date_to:datetime=None,
    ) -> dict[str, float | int]:
        result = {
                'capex': {
                    'operations_count': 0,
                    'total_amount': 0,
                },
                'opex': {
                    'operations_count': 0,
                    'total_amount': 0,
                },
            }
        rows = await self.db.get_investment_v2(user_id, date_from, date_to)
        for r in rows:
            result[r['mode']] = {
                'operations_count': int(r['operations_count']),
                'total_amount': round(float(r['total_amount']), 2),
            }
        return result
    
    async def get_investment_metrics(
        self, 
        user_id: int, 
        date_from: datetime=None, 
        date_to:datetime=None,
        mode:str='opex', 
    ) -> float:
        """
        Получить сумму финансовых операций по выбранному типу.

        Args:
            user_id (int):
                Идентификатор пользователя.

            date_from (datetime | None):
                Начальная дата периода.

            date_to (datetime | None):
                Конечная дата периода.

            mode (str):
                Тип операций для выборки.
                По умолчанию используется 'opex'.
                Для капитальных затрат используется 'capex'.

        Returns:
            float:
                Общая сумма операций выбранного типа за период.
        """
        rows = await self.db.get_investment(
            user_id=user_id,
            date_from=date_from,
            date_to=date_to,
            mode=mode
        )
        total_investment = sum(r['amount'] for r in rows)
        return round(float(total_investment), 2)