from core.base_db import Base
from backend.api.routers.investments.investments_and_expenses.schemas import InvestmentExpenseCreateSchema
from backend.api.routers.investments.investments_and_expenses.db import InvestmentsDB
from datetime import datetime


class InvestmentsAndExpensesRepository:
    """Репозиторий для управления финансовыми записями (инвестициями и расходами) в БД.

    Обеспечивает низкоуровневую работу с таблицами CAPEX и OPEX, выполняя 
    прямые SQL-запросы через специализированный класс базы данных.

    Attributes:
        db (InvestmentsDB): Экземпляр класса для работы с подключениями 
            к финансовой базе данных.
    """
    def __init__(self, base_db: "Base"):
        self.db = InvestmentsDB(base_db)

    
    async def create_operations(self, user_id: int, data: InvestmentExpenseCreateSchema):
        """Парсит входные финансовые данные и сохраняет каждую операцию в базу данных.

        Метод конвертирует дату в объект datetime, фильтрует системные поля
        и пустые значения, после чего последовательно записывает каждый ненулевой 
        финансовый показатель (CAPEX/OPEX) как отдельную строку в БД.

        Args:
            user_id: Идентификатор пользователя, совершившего операцию.
            data: Валидированная Pydantic-схема с данными о расходах (InvestmentExpenseCreateSchema).

        Returns:
            None
        """
        payload = data.model_dump()

        expense_date = datetime.strptime(data.expense_date, "%d.%m.%Y")
        
        # Перебираем все финансовые показатели, переданные в форме
        for key, val in payload.items():
            # Пропускаем метаданные и системные поля — они не являются суммами расходов
            if key in {'station_id', 'comment', 'mode', 'expense_date'}:
                continue
            # Пропускаем незаполненные поля (те расходы, по которым не было ввода)
            if val is None:
                continue
            
            # Сохраняем каждый конкретный тип расхода (например, 'rent_payment') отдельной строкой
            await self.db.insert(
                user_id=user_id,
                station_id=data.station_id,
                mode=data.mode,
                amount_type=key, # Имя поля из схемы становится типом расхода в БД
                amount=val, # Значение расхода
                comment=data.comment,
                expense_date=expense_date
            )