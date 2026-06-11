from backend.schemas.connect_operator import ConnectOperator
from backend.dependencies.get_manager import get_manager, get_current_token
from backend.database.manager import Manager
from core.logger.logger import make_logger
from core.security import security
from fastapi import APIRouter
from fastapi import Depends
from dotenv import load_dotenv
import os
from fastapi import HTTPException, status
load_dotenv()
logger = make_logger(__name__, use_telegram=False)
   



router = APIRouter(prefix='/operators', tags=['operators'])

@router.post("/connect", status_code=status.HTTP_201_CREATED)
async def connect(
    operator: ConnectOperator, 
    payload = Depends(get_current_token),
    db_manager: Manager=Depends(get_manager), 
):
    role = payload.get('role')
    if role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='У вас нет доступа к этому разделу'
        )
    
    user_data = await db_manager.connect_operator.check_user_existence(email=operator.email)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Инвестор не зарегестрирован'
        )
    
    user_id = user_data['id']

    auth_type = 'basic'
    if operator.operator != 'volt':
        auth_type = 'bearer'

    # шифруем парооли 
    encrypt_password = security.encrypt_data(operator.password)
    encrypt_login = security.encrypt_data(operator.login)

    # добавляем пользователя
    await db_manager.connect_operator.upsert_user_api_keys(
        user_id=user_id,
        auth_type=auth_type,
        login=encrypt_login,
        password=encrypt_password,
        operator=operator.operator
    )
    
    return {
        "detail": "Оператор подключен"
    }
    