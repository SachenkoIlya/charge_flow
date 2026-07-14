from frontend.utils.utils import utils
from fastapi import Request

def get_token_from_request(request: Request = None):
    if not request:
        return {}
    data_dict = utils.current_user.get_current_user(request=request)
    token = data_dict['token']
    if not token:
        return None
    return token
