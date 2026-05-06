from nicegui import ui, app
from datetime import datetime
from core.logger.logger import make_logger

logger = make_logger(__name__, use_telegram=False)


async def get_calendar(page_key:str, on_change_date=None):
    today = datetime.now().strftime('%d.%m.%Y')
    with ui.row().classes('items-center gap-3 justify-center'):
        page = app.storage.user.get('pages', {})
        logger.debug(page)
        page_state = page.get(page_key)
        date_from = page_state.get('date_from')
        date_to = page_state.get('date_to')
        logger.debug(page_state)
        
        value = (
            f'{date_from} - {date_to}' 
            if date_from and date_to 
            else f'{today} - {today}'
        )
        
        date_input = ui.input(
            label='Выберите диапазон',
            value=value
        ).props('dense borderless label-color=primary')\
         .classes('w-56 bg-white rounded-md px-3 text-gray-800')
        
        async def reset_dates_local():
            page = app.storage.user.get('pages')
            logger.debug(page)
            
            page_state = app.storage.user.get('pages', {}).get(page_key)
            
            page_state['date_from'] = today
            page_state['date_to'] = today
            app.storage.user['pages'][page_key] = page_state

            if on_change_date:
                await on_change_date()

        ui.button(icon='close', on_click=reset_dates_local)\
            .props('flat dense round')\
            .classes('-ml-10')
        
        with ui.menu().classes('anchor=bottom middle self=top middle'):
            date_picker = ui.date().props('range mask=DD.MM.YYYY')
            # биндим отображение в input
            date_picker.bind_value(
                date_input,
                forward=lambda x: (
                    f'{x["from"]} - {x["to"]}'
                    if isinstance(x, dict)
                    else x)
            )
            async def on_date_change(e):
                value = e.args[0]
                if value is None:
                    return
                
                logger.debug(f"value calendar: {value}".upper())
                today = datetime.now().strftime('%d.%m.%Y')

                date_from = None
                date_to = None
                
                if isinstance(value, str):
                    date_from = value
                    date_to = value
                    
                elif isinstance(value, dict):
                    date_from = value.get('from')
                    date_to = value.get('to')
                
                if not date_from:
                    date_from = today
                if not date_to:
                    date_to = today
                
                page = app.storage.user.get('pages', {})
                page_state = page.get(page_key)
                
                page_state['date_from'] = date_from
                page_state['date_to'] = date_to
                app.storage.user['pages'][page_key] = page_state

                logger.debug(f"Применили даты, пишем в storage".upper())
                logger.debug(app.storage.user)
                if on_change_date:
                    await on_change_date()
                print('Применили:', date_from, date_to)

            # 👉 слушаем date, НЕ input
        date_picker.on('update:model-value', on_date_change)
