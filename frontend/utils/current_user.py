from fastapi import Request
from core.security.security import security
from nicegui import app


class CurrentUser:
    @staticmethod
    def get_current_user(request: Request) -> dict | None:
        token = request.cookies.get('access_token')
        if not token:
            return {
                'token': None,
                'payload': None
            }

        payload = security.decode_token(token)
        if not payload:
            return {
                'token': token,
                'payload': None
            }
        return {
            'token': token,
            'payload': payload
        }