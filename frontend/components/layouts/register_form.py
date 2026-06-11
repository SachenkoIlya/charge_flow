from nicegui import ui
from frontend.utils.utils import utils
from frontend.api.client import frontend_api
import traceback
import httpx
import asyncio  

class RegisterForm:
    endpoints_name = 'auth_register'
    async def render(self):
        
        """
        Отрисовывает форму регистрации пользователя.

        Создаёт UI-контейнер с полями ввода данных:
        - имя
        - email
        - пароль
        - подтверждение пароля
        - компания
        - телефон

        Добавляет кнопку отправки формы и обработчик нажатия Enter,
        который также инициирует отправку формы.

        Внизу отображается ссылка для перехода на страницу входа
        для уже зарегистрированных пользователей.

        :return: None
        """
        container = ui.column().classes('w-full')
        with container:
            self.full_name = ui.input('Имя').classes('w-full')
            self.email = ui.input('Email').classes('w-full')
            self.password = ui.input('Пароль', password=True, password_toggle_button=True).classes('w-full')
            self.confirm = ui.input('Повторите пароль', password=True, password_toggle_button=True).classes('w-full')
            self.company = ui.input('Компания').classes('w-full')
            self.phone = ui.input(
                'Телефон',
                placeholder='+7 (___) ___-__-__'
            ).props('type=tel').classes('w-full')

            ui.button('Создать аккаунт', on_click=self.submit)
        container.on('keydown.enter', lambda e: self.submit())
      
        with ui.row().classes('justify-center items-center mt-3'):
            ui.label('Уже есть аккаунт?').classes('text-sm text-gray-500')
            ui.link('Войти', '/login').classes('text-sm ml-1')
     
    
    async def submit(self):
        """
        Обрабатывает отправку формы регистрации.

        Выполняет валидацию введённых данных:
        - проверяет заполненность всех полей
        - проверяет длину пароля (не менее 6 символов)
        - проверяет совпадение пароля и подтверждения
        - нормализует и валидирует номер телефона

        При успешной валидации формирует payload и отправляет POST-запрос
        на эндпоинт `auth/register`.

        Обрабатывает ответ сервера:
        - при успехе показывает уведомление и перенаправляет на страницу входа
        - при ошибке отображает сообщение об ошибке

        В случае исключения выводит ошибку в консоль.

        :return: None
        """
        if not all([
            self.full_name.value,
            self.email.value,
            self.password.value,
            self.confirm.value,
            self.company.value,
            self.phone.value
        ]):
            ui.notify('Заполните все поля', color='red')
            return
        # if not utils.is_valid_email(self.email.value):
        #     ui.notify('Некорректный email', color='red')
        #     return
        if len(self.password.value) < 6:
            ui.notify('Пароль слишком короткий', color='red')
            return
        if self.password.value != self.confirm.value:
            ui.notify('Пароли не совпадают', color='red')
            return
      
        phone_data = utils.normalize_phone.normalize_phone(phone=self.phone.value)
        if not phone_data:
            ui.notify('Некорректный номер телефона', color='red')
            return
        self.data = {
            "full_name": self.full_name.value,
            "email": self.email.value,
            "password": self.password.value,
            "company": self.company.value,
            "phone": phone_data['phone'],
            "country": phone_data['country_name']
            }
        await self.load_data()
    
    async def load_data(self):
        data = await frontend_api(
            endpoint_name=self.endpoints_name,
            payloads=self.data,
            # request=self.request
        )
        
        utils.logger.warning(data)
        if not data or data.get('error'):
            ui.notify('Сервер недоступен', color='red')
            return
            
        status_code = data['status_code']
        answer = data['data']

        if status_code == 401:
            ui.notify(answer.get('detail'), color='red')
            return
        if status_code == 403:
            ui.notify(answer.get('detail'), color='red')
            return
        if status_code == 400:
            ui.notify(answer.get('detail'), color='red')
            return
        if status_code >= 401:
            ui.notify(f'Ошибка: {status_code}', color='red')
            return

        ui.notify(answer.get('detail', 'Аккаунт создан'), color='green')
        await asyncio.sleep(2.5)
        ui.navigate.to('/login')