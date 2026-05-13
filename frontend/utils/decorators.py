from core.security.settings import settings

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .current_user import CurrentUser
from core.logger.logger import make_logger

from functools import  wraps
import traceback
from nicegui import app, ui
from dataclasses import dataclass

logger = make_logger(__name__, use_telegram=False)

@dataclass
class Auth:
    current_user: "CurrentUser"

    def require_auth(self, func):
        @wraps(func)    
        async def wrapper(*args, **kwargs):
            mode = settings.MODE
            try:
                data_dict = self.current_user.get_current_user(*args, **kwargs)
                user =  data_dict['payload']
                app.storage.user['user'] = user

                return await func(*args, **kwargs)
            except Exception as e:
                if mode in {'test', 'dev'}:
                    logger.error(f"{func.__name__}".upper())
                    logger.error(traceback.format_exc())
                    logger.error(str(e))
                app.storage.user.clear()
                app.storage.browser.clear() 
                ui.navigate.to('/login')
                return
        return wrapper  