from nicegui import ui
from ...components.filter_ccompany import get_filtered_company_from_admin

option = {
    'xAxis': {
      'type': 'category',
      'data': ['Пн', 'Вт', 'Ср', 'Чт', 'Пт']
    },
    'yAxis': {
      'type': 'value'
    },
    'series': [{
      'data': [120, 200, 150, 80, 70],
      'type': 'line',
    }]
  }

w_full = 'w-full'
classes = 'w-full max-w-[400px] p-6 rounded-xl shadow-md'
def get_calendar_card(func_calendar):
    with ui.column().classes(w_full):

      with ui.card().classes(classes):

          # 🔹 Заголовок
          ui.label("Период").classes(
              'text-xl font-semibold text-center mb-1'
          )

          # # 🔹 Подзаголовок (опционально)
          # ui.label("Выберите период для анализа").classes(
          #     'text-sm text-gray-500 text-center mb-1'
          # )

          # 🔹 Сам календарь
          with ui.row().classes('w-full  font-semibold text-center mb-1'):
              func_calendar()


def get_investor_choice():

  # with ui.column().classes(w_full):
  #     with ui.card().classes(classes):

  #         # 🔹 Заголовок
  #       ui.label("Выбор инвестора").classes(
  #           'text-xl font-semibold text-center mb-1'
  #       )

  with ui.row().classes('w-full  font-semibold text-center mb-1'):
    get_filtered_company_from_admin()