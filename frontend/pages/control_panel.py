from nicegui import ui, app
from fastapi import Request
from frontend.utils.utils import utils
from frontend.features.control_panel.panel import Panel
from frontend.utils.config import screen_background


@ui.page('/control_panel')
@utils.decorators.auth.require_auth
async def control_panel_page(request: Request):
  """
  Страница панели управления пользователя.
  Отображает основной интерфейс приложения, включающий:
  - верхнюю панель (header) с кнопкой меню, названием приложения и кнопкой выхода
  - боковое выдвижное меню (drawer) с элементами навигации
  Функциональность:
  - кнопка меню открывает/закрывает боковую панель
  - кнопка выхода перенаправляет пользователя на страницу входа
  - drawer содержит навигационные элементы (например, "Аналитика")
  :return: None
  """
  ui.page_title('📈 Dashboard')
  ui.query('body').classes(screen_background)
  user = app.storage.user.get('user')
  await Panel(user=user, request=request).render()
  
