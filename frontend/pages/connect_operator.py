from frontend.components.layouts.connect_operator_form import ConnectOperatorForm
from nicegui import ui, app
from fastapi import Request
from frontend.utils.utils import utils
from frontend.utils.config import screen_background

@ui.page('/operator')
async def connect_operator_page(request: Request):
    try:
        data_dict = utils.current_user.get_current_user(request=request)
        user = data_dict['payload']
    except Exception as e:
        utils.logger.error(str(e))
        app.storage.user.clear()
        app.storage.browser.clear() 
        ui.navigate.to('/login')
        return
    ui.query('body').classes(screen_background)
    print(ui.context.client.request.query_params)
    await ConnectOperatorForm(user=user, request=request).render()