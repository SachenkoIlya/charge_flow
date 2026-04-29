from nicegui import ui, app
from fastapi import Request
from frontend.utils.utils import utils
from frontend.features.control_panel.panel import Panel
from frontend.utils.config import screen_background
from dotenv import load_dotenv
import traceback
import os
load_dotenv()



@ui.page('/control_panel')
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
  mode = os.getenv('ETL_MODE')
  ui.page_title('📈 Dashboard')
  try:
    data_dict = utils.current_user.get_current_user(request=request)
    user = data_dict['payload']

  except Exception as e:
    if mode in {'test', 'dev'}:
      utils.logger.error(f"----control panel----".upper())
      utils.logger.error(traceback.format_exc())
    
    utils.logger.error(str(e))
    app.storage.user.clear()
    app.storage.browser.clear() 
    ui.navigate.to('/login')
    return

  ui.query('body').classes(
     screen_background
    # 'bg-gray-200 m-0 overflow-hidden'
    )
  
  await Panel(user=user, request=request).render()
  
