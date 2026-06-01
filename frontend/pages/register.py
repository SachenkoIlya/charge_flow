from nicegui import  ui
from frontend.components.layouts.register_form import RegisterForm
from frontend.components.setup_theme import setup_theme
from frontend.utils.config import screen_background


@ui.page('/register')
async def register_page():
    """
    Страница регистрации пользователя.

    Отображает форму регистрации с полями для ввода данных пользователя.
    Настраивает базовые стили страницы и центрирует карточку с формой.

    Содержимое страницы:
    - Заголовок "Регистрация"
    - Карточка с формой регистрации (RegisterForm)

    :return: None
    """
    setup_theme()
    ui.query('body').classes('bg-gray-100 m-0 overflow-hidden')
    with ui.column().classes(
        'w-full h-screen items-center justify-center'
    ):
        ui.label(
            'Регистрация'
        ).classes(
            'text-3xl font-extrabold text-gray-800 mb-6'
        )
        with ui.card().classes(
            'w-full max-w-md p-8 shadow-lg rounded-2xl'
        ):
            await RegisterForm().render()