from nicegui import ui
CARD = 'w-full justify-between items-start'
STYLE_COLUMN = 'gap-1 mb-10'
LABEL_REVENUE = 'Общий доход по всем локациям'
STYLE_REVENUE = 'text-3xl font-semibold text-gray-800'
LABEL_AGGRE = 'Агрегировано по всей сети станций'
STYLE_AGGRE = 'text-l font-semibold text-gray-500'

async def render_hight(label: str=None, style:str=None, label_aggre:str=None):
    label = label or LABEL_REVENUE
    style = style or STYLE_REVENUE
    label_aggre = label_aggre or LABEL_AGGRE
    with ui.row().classes(CARD):
        with ui.column().classes(STYLE_COLUMN):
            ui.label(label).classes(style)
            ui.label(label_aggre).classes()
                