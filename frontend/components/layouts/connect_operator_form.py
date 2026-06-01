from nicegui import ui
from frontend.utils.utils import utils
from frontend.api.client import frontend_api

from frontend.components.drawer import render_sidebar
from dataclasses import dataclass
from fastapi import Request


@dataclass
class ConnectOperatorForm:
    user: dict
    request: Request
    endpoints_name = 'operators_connect'
    page_ky = 'operators_connect'


    async def render(self):
        role = self.user.get('role')

        with ui.element('div').classes(
            """
                w-screen
                h-screen
                flex
                bg-gradient-to-br
                from-[#050b12]
                via-[#08111b]
                to-[#0b1724]
                text-white
                overflow-hidden
            """
        ):
            render_sidebar(role=role)

        with ui.element('div').classes(
            # 'w-full h-screen flex items-center justify-center'
            'w-full h-screen flex items-start justify-center pt-20'
        ):
            with ui.card().classes(
                'w-full max-w-md p-8 shadow-lg rounded-2xl gap-4'
               
            ):
        
        # 🔥 Заголовок
                ui.label('Подключение оператора').classes(
                    'text-xl font-semibold'
                )

                # 🔥 Описание
                ui.label(
                    'Введите email пользователя (инвестора) и данные оператора '
                    'для подключения к системе.'
                ).classes('text-sm text-gray-500')

                ui.separator()

                container = ui.column().classes('w-full gap-3')

            with container:
                # 🔹 Пользователь
                ui.label('Пользователь').classes('text-xs text-gray-400')
                self.email = ui.input(
                    'Email',
                    placeholder='email зарегистрированного пользователя'
                ).classes('w-full')

                # 🔹 Оператор
                ui.label('Данные оператора').classes('text-xs text-gray-400 mt-2')

                self.login = ui.input('Login').classes('w-full')

                self.operator = ui.input(
                    'Оператор',
                    placeholder='не обязательное поле'
                ).classes('w-full')

                self.password = ui.input(
                    'Пароль',
                    password=True,
                    password_toggle_button=True
                ).classes('w-full')

                ui.button(
                    'Подключить оператора',
                    on_click=self.submit
                ).classes('mt-4 w-full')

            container.on('keydown.enter', lambda e: self.submit())
       

    async def submit(self):
        if not all([
            self.email.value,
            self.password.value,
            self.login.value
        ]):
            ui.notify('Заполните все поля', color='red')
            return
        self.data = {
            'email': self.email.value,
            'password': self.password.value,
            'login': self.login.value
        }
        self.operators_connect()


    async def operators_connect(self):
        
        data = await frontend_api(
            endpoint_name=self.endpoints_name,
            payloads=self.data,
            request=self.request
        )
            
        if not data or data.get('error'):
            ui.notify('Сервер недоступен', color='red')
            return
            
        status_code = data['status_code']
        answer = data['data']

        if status_code == 401:
            ui.notify(answer.get('detail'), color='red')
            ui.navigate.to('/login')
            return

        if status_code == 403:
            ui.notify(answer.get('detail'), color='red')
            return

        if status_code >= 400:
            ui.notify(f'Ошибка: {status_code}', color='red')
            return
       
        ui.notify(answer.get('detail', 'Успешно'), color='green')