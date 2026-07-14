from frontend.components.setup_theme import setup_theme
from core.security.settings import settings
from nicegui import ui



class LoginForm:
    endpoint_name = 'auth_login'
    async def render(self):
        """
        Отрисовывает форму входа пользователя.

        Создаёт элементы интерфейса:
        - заголовок "Вход"
        - поле ввода email
        - поле ввода пароля с возможностью показать/скрыть
        - кнопку отправки формы
        - ссылку на страницу регистрации для новых пользователей

        При нажатии на кнопку вызывается метод submit.

        :return: None
        """
        setup_theme()
        container = ui.column().classes('w-full max-w-sm mx-auto')
        with container:
            ui.label('Вход').classes('text-xl font-bold')
            with ui.element('form').props(
               f'method=post action="{settings.BACKEND_URL}/v1/user/auth/login"'
            #    https://api.opower.su/v1/user/auth/login
            ).classes('w-full'):
                
                ui.input('Email').props('name=email').classes('w-full')

                ui.input(
                    'Пароль',
                    password=True,
                    password_toggle_button=False
                ).props('name=password').classes('w-full')

                ui.button('Войти').props('type=submit').classes('w-full mt-2')
            
            with ui.row().classes('justify-center mt-2'):
                ui.label('Нет аккаунта?').classes('text-sm text-gray-500')
                ui.link('Регистрация', '/register').classes('text-sm ml-1')
        
