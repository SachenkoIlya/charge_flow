from .normalize_phone import NormalizePhone
from .current_user import CurrentUser
from core.logger.logger import make_logger
class Utils:
    current_user = CurrentUser()
    normalize_phone = NormalizePhone()
    logger = make_logger(__name__, use_telegram=False)

utils = Utils()