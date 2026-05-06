from frontend.features.trends.panel import Panel
from nicegui import ui, app
from fastapi import Request
from frontend.utils.utils import utils
from frontend.utils.config import screen_background

@ui.page('/trends')
@utils.decorators.auth.require_auth
async def connect_operator_page(request: Request,  user: dict):
  
    ui.query('body').classes(screen_background)

    utils.logger.debug(f"рисуем trends: {user}")
    await Panel(user=user, request=request).render()