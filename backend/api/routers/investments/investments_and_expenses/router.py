from pydantic import BaseModel

from backend.manager.finance import ManagerFinance
from backend.dependencies.get_manager import get_current_token, get_merics_investment
from backend.api.routers.investments.investments_and_expenses.schemas import InvestmentExpenseCreateSchema, ResponseModel
from fastapi import APIRouter
from fastapi import Depends



ENDPOINT = '/investments-and-expenses'
description = """
Сохранение данных об инвестициях и расходах

Принимает и сохраняет пользовательский ввод из заполненных форм финансовых отчетов.

Поддерживаемые типы расходов:**
CAPEX - (Capital Expenditures) — капитальные затраты / инвестиции.
OPEX - (Operating Expenditures) — операционные расходы.
"""

router = APIRouter(
    prefix='/v1/finance', 
    tags=['finance']
)



@router.post(
    ENDPOINT, 
    description=description,
    response_model=ResponseModel
)
async def create(
    data: InvestmentExpenseCreateSchema,
    payload = Depends(get_current_token),
    metrics:  ManagerFinance=Depends(get_merics_investment)
):
    """Создает новую запись о расходах (CAPEX или OPEX) в системе.

    Извлекает идентификатор пользователя из токена авторизации, после чего
    передает финансовые данные в менеджер метрик для сохранения в БД.

    Args:
        data: Валидированные входные данные формы расходов (CAPEX/OPEX).
        payload: Данные декодированного JWT-токена текущего пользователя.
        metrics: Менеджер финансовых метрик для работы с бизнес-логикой.

    Returns:
        dict: Словарь с флагом успешности и текстовым уведомлением, 
            соответствующий схеме ResponseModel.
    """
    user_id = payload.get('user_id')

    await metrics.investments.create_operations(
        user_id=user_id, 
        data=data
    )

    return {
        "success": True,
        "message": "Данные успешно сохранены"
    }