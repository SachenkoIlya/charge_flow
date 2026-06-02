from nicegui import ui
from core.logger.logger import logger
from frontend.features.investments_and_expenses.schemas.schemas import resolve_model
from frontend.api.client import frontend_api
from fastapi import Request


EXPENSES_MAP = {
    'opex': {
        'electricity_compensation': 'Компенсация электроэнергии',
        'rent_payment': 'Арендная плата',
        'operator_commission': 'Комиссия оператору',
        'internet_and_connection': 'Интернет и связь',
        'taxes': 'Налоги',
        'insurance': 'Страхование',
        'service_maintenance': 'Сервисное обслуживание',
        'other_expenses': 'Прочие расходы',
        # 'comment': 'Комментарий'
    },

    'capex': {
        'location_search': 'Поиск и согласование локации',
        'equipment_purchase': 'Приобретение оборудования (ЭЗС)',
        'construction_and_installation': 'СМР и пусконаладочные работы',
        'other_capex': 'Прочие капитальные расходы',
        # 'comment': 'Комментарий'
    },
}

SELECTED_STATION = {
    '2': 'Станция 1',
    '3': 'Станция 2',
    '4': 'Станция 3'
}

def prepare_station(selected_station: list[dict]) -> dict:
    return  {
        str(station_id): f"{s['label']} · {station_key}"
        for s in selected_station
        for station_id, station_key 
        in zip(
            s['station_ids'],
            s['station_keys']
        )
    }

async def get_selected_station(
    request: Request, 
    endpoint_name:str='stations'
) -> list[dict]:
    
    selected_station = await frontend_api(
        endpoint_name=endpoint_name,
        request=request,
    )
    return prepare_station(selected_station)




async def render_form(data: dict[str, list], request: Request, mode:str = 'opex'):
    inputs = {}
    category = data.get(mode)

    selected_station = await get_selected_station(request=request)

    
    logger.debug(f"selected_station_t: {selected_station}")

    async def submit():
        payload = {
            key: input_.value
            for key, input_ in inputs.items()
        }
        if payload.get('station_id') is None:
            ui.notify(
                'Выберите станцию',
                color='red'
            )
            return
        model = resolve_model(payload, mode)
        logger.debug(model)


    with ui.element('main').classes(
        'flex-1 h-screen flex items-start justify-center pt-10 pr-24'
    ):
        with ui.card().classes(
            '''
            w-full
            max-w-2xl
            p-8
            
            shadow-xl
            rounded-2xl
            gap-5
            border
            border-green-500/40
            bg-[#101923]/90
            text-white
            '''
        ):
            with ui.column().classes('w-full gap-1 mb-4'):
                ui.label(f'{mode.upper()}').classes(
                    'text-2xl font-bold text-white'
                )
                ui.label(
                    'Заполните статьи расходов для финансовой модели'
                ).classes(
                    'text-xl text-gray-400'
                )
                ui.label(
                    'Указывайте суммы только цифрами, без пробелов и текста.'
                ).classes(
                    'text-l text-gray-500'
                )

            ui.separator().classes('bg-[#1f2937]')

            with ui.column().classes('w-full gap-3') as container:
                
                inputs['station_id'] = ui.select(
                    selected_station,
                    label='Cтанция',
                    with_input=True
                ).props('dense').classes('w-full')
    
                for key, label in category.items():
                    inputs[key] = ui.input(
                        label=label,
                        placeholder='Введите сумму'
                    ).classes(
                        'w-full'
                    ).props(
                        'dense'
                    )

                # inputs['comment'] = ui.textarea(
                #     label='Комментарий',
                #     placeholder='Необязательный комментарий',
                # ).props(
                #     'filled counter max_length=250'
                # ).classes(
                #     'w-full'
                # )

                ui.button(
                    'Применить',
                    on_click=submit
                ).classes(
                    'mt-4 w-full'
                )