from core.logger.logger import logger
from nicegui import ui, app
from core.http.services.exception import (
    APIError, 
    UnauthorizedError,
    ForbiddenError,
    NotFoundError,
    ServerError
)

async def handle_frontend_api_error(error: Exception):
    logger.exception(error)

    if isinstance(error, UnauthorizedError):
        app.storage.user.clear()
        app.storage.browser.clear()
        ui.notify('Сессия истекла', color='red')
        ui.navigate.to('/login')
        return

    if isinstance(error, ForbiddenError):
        ui.notify('Нет доступа', color='red')
        return

    if isinstance(error, NotFoundError):
        ui.notify('Данные не найдены', color='orange')
        return

    if isinstance(error, ServerError):
        ui.notify('Ошибка сервера', color='red')
        return

    if isinstance(error, APIError):
        ui.notify('Ошибка API', color='red')
        return

    ui.notify('Сервер недоступен', color='red')