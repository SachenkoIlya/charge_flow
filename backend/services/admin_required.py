from backend.database.get_manager import get_current_token
from core.security import security
from fastapi import Depends, HTTPException


def admin_required(payload: dict = Depends(get_current_token)):
    if payload.get('role') != 'admin':
        raise HTTPException(status_code=403, detail="Forbidden")