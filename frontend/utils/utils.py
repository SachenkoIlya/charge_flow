from .normalize_phone import NormalizePhone
from .current_user import CurrentUser
from core.logger.logger import make_logger
from frontend.utils.decorators import Auth
from dataclasses import  dataclass

@dataclass
class Decorators:
    logger: make_logger
    current_user: "CurrentUser"
    
    auth = Auth(logger, current_user)




class Utils:
    current_user = CurrentUser()
    normalize_phone = NormalizePhone()
    logger = make_logger(__name__, use_telegram=False)
    decorators =Decorators(logger, current_user)
    
utils = Utils()
