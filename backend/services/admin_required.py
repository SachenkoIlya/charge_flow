from backend.dependencies.get_manager import get_current_token
from fastapi import Depends, HTTPException


def admin_required(payload: dict = Depends(get_current_token)):
    if payload.get('role') != 'admin':
        raise HTTPException(status_code=403, detail="Forbidden")