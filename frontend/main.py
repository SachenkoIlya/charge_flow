from nicegui import ui
from nicegui import app

import frontend.pages.login
import frontend.pages.register
import frontend.pages.control_panel
import frontend.pages.connect_operator

from dotenv import load_dotenv
import os
load_dotenv()


app.add_static_files('/media', 'frontend/components/media')

@ui.page('/')
def root():
        ui.navigate.to('/login')

ui.run(
    language='ru',
    storage_secret=os.getenv('SECRET_KEY_FROM_UI'),
    host=os.getenv('FRONTEND_HOST', '0.0.0.0'),
    port=int(os.getenv('FRONTEND_PORT', 8080)),
)
# C:\Users\Ilya\Desktop\ChargeFlow\frontend\main.py

# py -m frontend.main