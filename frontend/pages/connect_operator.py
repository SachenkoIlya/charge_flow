from frontend.components.layouts.connect_operator_form import ConnectOperatorForm
from nicegui import ui, app
from fastapi import Request
from frontend.components.setup_theme import setup_theme
from frontend.utils.utils import utils
from frontend.utils.config import screen_background


@ui.page('/operator')
@utils.decorators.auth.require_auth
async def connect_operator_page(request: Request):
    setup_theme()
    user = app.storage.user.get('user')
    ui.query('body').classes(screen_background)
    await ConnectOperatorForm(user=user, request=request).render()