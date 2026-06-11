from backend.core.schemas import DashboardFilterSchema
from core.logger.logger import logger

def get_valid_id(role:str, data: DashboardFilterSchema, user_id: int) -> int:
    valid_id = None
    if role == 'admin':
        logger.debug(f"role: {role}, используем id: {data.company_id}".upper())
        valid_id = data.company_id
    else:
        logger.debug(f"role: {role}, используем id: {user_id}".upper())
        valid_id = user_id
    return valid_id