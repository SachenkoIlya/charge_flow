from nicegui import ui

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
