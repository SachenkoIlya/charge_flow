from core.base_db import Base
from backend.api.routers.investments.investments_and_expenses.schemas import InvestmentExpenseCreateSchema
from backend.api.routers.investments.investments_and_expenses.db import InvestmentsDB
from datetime import datetime


class InvestmentsAndExpensesRepository:
    def __init__(self, base_db: "Base"):
        self.db = InvestmentsDB(base_db)

    
    async def create_operations(self, user_id: int, data: InvestmentExpenseCreateSchema):
        payload = data.model_dump()

        expense_date = datetime.strptime(data.expense_date, "%d.%m.%Y")
        for key, val in payload.items():
            if key in {'station_id', 'comment', 'mode', 'expense_date'}:
                continue
            if val is None:
                continue
            
            await self.db.insert(
                user_id=user_id,
                station_id=data.station_id,
                mode=data.mode,
                amount_type=key,
                amount=val,
                comment=data.comment,
                expense_date=expense_date
            )