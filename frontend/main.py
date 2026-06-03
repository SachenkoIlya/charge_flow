from core.security.settings import settings
from nicegui import ui
from nicegui import app

import frontend.pages.login
import frontend.pages.register
import frontend.pages.control_panel
import frontend.pages.connect_operator
import frontend.pages.trends
import frontend.pages.summary
import frontend.pages.finance
import frontend.pages.investments_and_expenses
import frontend.pages.system_monitoring





app.add_static_files('/media', 'frontend/components/media')



@ui.page('/')
def root():
        ui.navigate.to('/login')

ui.run(
    language='ru',
    dark=True,
    storage_secret=settings.SECRET_KEY_FROM_UI,
    host=settings.FRONTEND_HOST,
    port=settings.FRONTEND_PORT
)

# py -m frontend.main