from nicegui import ui
CARD = 'w-full justify-between items-start'
STYLE_COLUMN = 'gap-1 mb-10'
LABEL_REVENUE = 'Общий доход по всем локациям'
STYLE_REVENUE = 'text-3xl font-semibold text-gray-800'
LABEL_AGGRE = 'Агрегировано по всей сети станций'
STYLE_AGGRE = 'text-l font-semibold text-gray-500'


LEFT_WRAPPER_STYLE = 'flex: 2.5; min-width: 0; display: flex'
CARD_CLASSES = 'p-6 w-full'
CARD_STYLE = 'flex: 1'


# def title(label: str=None, style:str=None, label_aggre:str=None):
#     label = label or LABEL_REVENUE
#     style = style or STYLE_REVENUE
#     label_aggre = label_aggre or ""
#     with ui.row().classes(CARD):
#         with ui.column().classes(STYLE_COLUMN):
#             ui.label(label).classes(style)
#             ui.label(label_aggre).classes()
                

def render_title(label: str = None, style: str = None, label_aggre: str = None):
    label = label or 'Общая сводка по сети'
    label_aggre = label_aggre or 'Executive Dashboard'

    with ui.column().classes('mb-6'):
        ui.label(label).classes('text-3xl font-bold text-white')
        ui.label(label_aggre).classes('text-sm text-gray-400')