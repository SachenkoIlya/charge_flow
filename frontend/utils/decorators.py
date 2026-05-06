from core.security.settings import settings

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .current_user import CurrentUser
    from core.logger.logger import make_logger

from functools import  wraps
import traceback
from nicegui import app, ui
from dotenv import load_dotenv
import os
load_dotenv()
from dataclasses import dataclass


@dataclass
class Auth:
    current_user: "CurrentUser"
    logger: make_logger

    def require_auth(self, func, ut):
        @wraps(func)    
        async def wrapper(*args, **kwargs):

            mode = settings.MODE
            try:
                data_dict = self.current_user.get_current_user(*args, **kwargs)
                user =  data_dict['payload']
                kwargs['user'] = user

                return await func(*args, **kwargs)
            except Exception as e:
                if mode in {'test', 'dev'}:
                    self.logger.error(f"----control panel----".upper())
                    self.logger.error(traceback.format_exc())
                    self.logger.error(str(e))
                app.storage.user.clear()
                app.storage.browser.clear() 
                ui.navigate.to('/login')
                return
        return wrapper  