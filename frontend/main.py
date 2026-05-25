from nicegui import ui
from nicegui import app

import frontend.pages.login
import frontend.pages.register
import frontend.pages.control_panel
import frontend.pages.connect_operator
import frontend.pages.trends

from dotenv import load_dotenv
import os
load_dotenv()


def setup_theme():
    ui.colors(
        primary='#22c55e',
        secondary='#38bdf8',
        accent='#8b5cf6',
        positive='#22c55e',
        negative='#ef4444',
        warning='#f97316',
    )

    ui.add_head_html('''
    <style>
    body, .q-page {
        background: #070d14;
        color: #e5e7eb;
    }

    .dark-card {
        background: linear-gradient(145deg, #111923, #0b111a);
        border: 1px solid #1f2937;
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.25);
        color: #e5e7eb;
    }

    .dark-sidebar {
        background: #071019;
        border-right: 1px solid #1f2937;
        color: #e5e7eb;
    }

    .muted {
        color: #9ca3af;
    }

    .green-text {
        color: #22c55e;
    }
    </style>
    ''')


app.add_static_files('/media', 'frontend/components/media')

setup_theme()

@ui.page('/')
def root():
        ui.navigate.to('/login')

ui.run(
    language='ru',
    dark=True,
    storage_secret=os.getenv('SECRET_KEY_FROM_UI'),
    host=os.getenv('FRONTEND_HOST', '0.0.0.0'),
    port=int(os.getenv('FRONTEND_PORT', 8080)),
)

# py -m frontend.main