from nicegui import ui

from frontend.components.calendar import get_calendar
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
                

async def render_title(
    label: str, 
    label_aggre: str,
    page_key: str,
    on_date_change=None,

):
    with ui.row().classes('w-full items-start justify-between mb-6'):

        with ui.column().classes('gap-0'):
            ui.label(label).classes(
                'text-3xl font-bold text-white leading-tight'
            )

            ui.label(label_aggre).classes(
                'text-sm text-gray-400 mt-1'
            )

        await get_calendar(
            page_key=page_key,
            on_change_date=on_date_change,
        )
    