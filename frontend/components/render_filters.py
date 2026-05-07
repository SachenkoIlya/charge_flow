from nicegui import ui

from frontend.components.calendar import get_calendar
from frontend.components.filters import get_filtered_data

async def render_filters(apply_filters, request, page_key, refresh, role):
    with ui.dialog() as dialog:
        async def apply_and_close():
            apply_filters()
            await refresh()
            dialog.close()

        with ui.card().classes(
            'w-[640px] min-h-[360px] p-6 rounded-xl shadow-2xl gap-6'
        ):
                # Header
            with ui.row().classes('w-full items-center justify-between'):
                ui.label('Фильтры').classes(
                    'text-2xl font-semibold'
                )
                ui.button(
                    icon='close',
                    on_click=dialog.close
                ).props('flat round dense')

                # Filters block
                
                with ui.column().classes('w-full gap-5'):
                    if role == 'admin':
                        await get_filtered_data(
                            request=request, 
                            endpoint_name ='company',
                            label='Компании',
                            page_key=page_key
                        )
                    await get_filtered_data(
                            request=request, 
                            endpoint_name ='station',
                            label='Станции',
                            page_key=page_key
                        )
                    with ui.column().classes('w-full gap-2'):
                        ui.label('Период').classes(
                            'text-sm text-gray-500 font-medium'
                        )

                        with ui.card().classes(
                             'w-full bg-gray-50 rounded-xl p-4'
                        ):
                            await get_calendar(
                                page_key=page_key,
                                # on_change_date=self.on_date_change,
                            )

                ui.separator()

                # Footer
                with ui.row().classes(
                    'w-full justify-end gap-3 pt-2'
                ):
                    ui.button(
                        'Отмена',
                        on_click=dialog.close
                    ).props('flat')

                    ui.button(
                        'Применить',
                        on_click=apply_and_close
                    ).props('unelevated color=primary')

        # Кнопка открытия фильтров
        ui.button(
            'Фильтры',
            icon='tune',
            on_click=dialog.open,
        ).props('flat color=white')
