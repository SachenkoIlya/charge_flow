from pydantic import BaseModel

from backend.api.routers.dashboard.manager import ManagerFinance
from backend.database.get_manager import get_current_token, get_merics_investment
from backend.api.routers.investments.investments_and_expenses.schemas import InvestmentExpenseCreateSchema
from fastapi import APIRouter
from fastapi import Depends




router = APIRouter(prefix='/finance', tags=['finance'])

class ResponseModel(BaseModel):
    success: bool
    message: str


@router.post('/investments-and-expenses', response_model=ResponseModel)
async def create(
    data: InvestmentExpenseCreateSchema,
    payload = Depends(get_current_token),
    metrics:  ManagerFinance=Depends(get_merics_investment)
):
    user_id = payload.get('user_id')

    await metrics.investments_and_expenses.create_operations(
        user_id=user_id, 
        data=data
    )

    return {
        "success": True,
        "message": "Данные успешно сохранены"
    }