from nicegui import  ui
from frontend.components.layouts.login_form import LoginForm
from frontend.utils.utils import utils
from fastapi import Request 


async def login(request: Request):
    utils.logger.debug('--- REQUEST DEBUG ---')

    utils.logger.debug(f"URL: {request.url}")
    utils.logger.debug(f"METHOD: {request.method}")

    utils.logger.debug(f"HEADERS: {dict(request.headers)}")

    utils.logger.debug(f"COOKIES: {request.cookies}")

    form = await request.form()
    utils.logger.debug(f"FORM DATA: {dict(form)}")


@ui.page('/login')
async def login_page(request: Request):
    """
    Страница входа пользователя.

    Настраивает стили страницы и отображает форму авторизации,
    центрированную по вертикали и горизонтали.

    Содержимое страницы:
    - контейнер с ограниченной шириной
    - форма входа (LoginForm)

    :return: None
    """
    await login(request=request)
    errors = {
        'missing_fields': 'Заполните все поля',
        'invalid_email': 'Некорректный e-mail',
        'invalid_credentials': 'Неверный логин или пароль'
    }
    error = ui.context.client.request.query_params.get('error')

    utils.logger.debug(f"query_params: {ui.context.client.request.query_params}")
    utils.logger.debug(error)
    
    # for client in Client.instances.values():
    #     try:
    #         utils.logger.debug(f"CLIENT: {client}")
    #         utils.logger.debug(f"SESSION:, {getattr(client.request, 'session', None)}")
    #     except Exception as e:
    #         utils.logger.warning(f"ERROR: {e}")

    if error:
        ui.notify(f"{errors.get(error)}", color='red')
        # ui.run_javascript('history.replaceState(null, "", "/login")')
    ui.query('body').classes('bg-gray-100 m-0 overflow-hidden')
    with ui.column().classes(
        'w-full h-screen items-center justify-center'
    ):
        with ui.column().classes('w-full max-w-sm p-6'):
            await LoginForm().render()


