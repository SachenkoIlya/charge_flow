from frontend.components.stat_card import stat_card
from nicegui import ui

DIV = 'div'
CARD = 'width: 30%; padding: 0;'
STYLE = 'display: grid; grid-template-rows: repeat(4, 1fr); gap: 12px; height: 100%'
    

async def render_right(metrics: dict):
    with ui.element(DIV).style(CARD):
        with ui.element(DIV).style(STYLE):
            for m in metrics['extra']:
                stat_card(
                    label=m['label'],
                    value=m['value'],
                    gradient=m.get('color')
                )
