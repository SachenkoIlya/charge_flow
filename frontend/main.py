from nicegui import ui

import frontend.pages.login
import frontend.pages.register
import frontend.pages.control_panel
import frontend.pages.connect_operator

from dotenv import load_dotenv
import os
load_dotenv()

@ui.page('/')
def root():
        ui.navigate.to('/login')

ui.run(
    language='ru',
    storage_secret=os.getenv('SECRET_KEY_FROM_UI'),
    host='0.0.0.0', 
    port=8080
)
# C:\Users\Ilya\Desktop\ChargeFlow\frontend\main.py

# py -m frontend.main