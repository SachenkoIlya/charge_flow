from nicegui import ui
from core.logger.logger import logger
from frontend.features.investments_and_expenses.schemas.schemas import schemas
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
    },

    'capex': {
        'location_search': 'Поиск и согласование локации',
        'equipment_purchase': 'Приобретение оборудования (ЭЗС)',
        'construction_and_installation': 'СМР и пусконаладочные работы',
        'other_capex': 'Прочие капитальные расходы',
    },
}

SELECTED_STATION = {
    '1': 'Все станции',
    '2': 'Станция 1',
    '3': 'Станция 2',
    '4': 'Станция 3'
}


def resolve_model(payload:dict, mode:str):
    schema = schemas.get(mode)
    return schema.model_validate(payload)


async def render_form(data: dict[str, list], selected_station:dict, mode:str = 'opex'):
    inputs = {}
    category = data.get(mode)
    async def submit():
        payload = {
            key: input_.value
            for key, input_ in inputs.items()
        }
        logger.debug(payload)
        model = resolve_model(payload, mode)
        logger.debug(model)

        
    with ui.element('main').classes(
        'flex-1 h-screen flex items-start justify-center pt-16'
    ):
        with ui.card().classes(
            '''
            w-full
            max-w-2xl
            p-8
            shadow-xl
            rounded-2xl
            gap-5
            bg-[#101923]/90
            border border-[#1f2937]
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
                    'text-sm text-gray-400'
                )

            ui.separator().classes('bg-[#1f2937]')

            with ui.column().classes('w-full gap-3') as container:
                inputs['station_id'] = ui.select(
                    selected_station,
                    label='Cтанция',
                    with_input=True
                ).props('outlined dense').classes('w-full')
    
                for key, label in category.items():
                    inputs[key] = ui.input(
                        label=label,
                        placeholder='Введите сумму'
                    ).classes(
                        'w-full'
                    ).props(
                        'dense outlined'
                    )

                ui.button(
                    'Применить',
                    on_click=submit
                ).classes(
                    'mt-4 w-full'
                )