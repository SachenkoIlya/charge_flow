from backend.api.routers.widget.charts.db import ChartsDB
from datetime import datetime



class NetworkCostStructureChart:
    """
    Сервис подготовки данных для финансовых графиков и диаграмм.

    Отвечает за получение агрегированных данных из БД и преобразование
    их в формат, удобный для отображения на дашборде.

    Основные задачи:
    - подготовка структуры операционных расходов (OPEX);
    - агрегация данных для круговых и столбчатых диаграмм;
    - формирование единого формата ответа для UI.

    Attributes:
        db (FinanceDB):
            Слой доступа к финансовым данным.
    """
    def __init__(self, chart_db: "ChartsDB"):
        self.db = chart_db
        self.chart_name: str = 'network_cost_structure'
        
    async def get_network_cost_structure(
        self, 
        user_id:int,
        date_from:datetime=None, 
        date_to:datetime=None,
        
    ) -> dict:
        """
        Получить структуру сетевых расходов за выбранный период.

        Метод агрегирует расходы по категориям и возвращает данные
        в формате, пригодном для построения диаграммы структуры затрат.

        Категории расходов:
            - electricity_compensation;
            - rent_payment;
            - operator_commission;
            - service_maintenance;
            - internet_and_connection;
            - taxes.

        Args:
            user_id (int):
                Идентификатор пользователя.

            date_from (datetime | None):
                Начальная дата периода.

            date_to (datetime | None):
                Конечная дата периода.

            chart_name (str):
                Имя графика в итоговой структуре ответа.

        Returns:
            dict:
                Словарь с данными для диаграммы.

                Пример:
                {
                    "network_cost_structure": {
                        "electricity_compensation": 165000.0,
                        "rent_payment": 59000.0,
                        "operator_commission": 85000.0,
                        "service_maintenance": 4000.0,
                        "internet_and_connection": 1150.0,
                        "taxes": 12000.0
                    }
                }
        """
        result = {
            'electricity_compensation': 0,
            'rent_payment': 0,
            'operator_commission': 0,
            'service_maintenance': 0,
            'internet_and_connection': 0,
            'taxes': 0
        }

        rows = await self.db.get_network_cost_structure(
            user_id=user_id,
            date_from=date_from,
            date_to=date_to
        )
        if rows:
            row = rows[0]
            result.update({
                key: round(float(row[key] or 0), 2)
                for key in result
            })
        return {
            self.chart_name: result
        }

    async def get_cost_structure(
        self, 
        user_id: int, 
        date_from:datetime=None, 
        date_to:datetime=None
    ):
        """
        Получить данные для диаграммы структуры затрат.

        Является публичной точкой входа для формирования графика
        распределения операционных расходов.

        Args:
            user_id (int):
                Идентификатор пользователя.

            date_from (datetime | None):
                Начальная дата периода.

            date_to (datetime | None):
                Конечная дата периода.

        Returns:
            dict:
                Структура данных для отображения диаграммы затрат.
        """
        return await self.get_network_cost_structure(
            user_id=user_id,
            date_from=date_from,
            date_to=date_to
        )