from nicegui import ui, app
from fastapi import Request
from frontend.components.setup_theme import setup_theme
from frontend.utils.utils import utils
from frontend.features.system_monitoring.panel import Panel
from frontend.utils.config import screen_background


@ui.page('/system_monitoring')
@utils.decorators.auth.require_auth
async def system_monitoring_page(request: Request):
    setup_theme()
    ui.page_title('📈 Dashboard')
    ui.query('body').classes(screen_background)
    user = app.storage.user.get('user')
    await Panel(user=user, request=request).render()
    

