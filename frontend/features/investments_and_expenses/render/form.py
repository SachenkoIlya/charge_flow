from nicegui import ui
from frontend.features.investments_and_expenses.render.submit import submit
EXPENSES_MAP = {
    'OPEX': {
        'electricity_compensation': 'Компенсация электроэнергии',
        'rent_payment': 'Арендная плата',
        'operator_commission': 'Комиссия оператору',
        'internet_and_connection': 'Интернет и связь',
        'taxes': 'Налоги',
        'insurance': 'Страхование',
        'service_maintenance': 'Сервисное обслуживание',
        'other_expenses': 'Прочие расходы',
    },

    'CAPEX': {
        'location_search': 'Поиск и согласование локации',
        'equipment_purchase': 'Приобретение оборудования (ЭЗС)',
        'construction_and_installation': 'СМР и пусконаладочные работы',
        'other_capex': 'Прочие капитальные расходы',
    },
}


def render_form(data: dict[str, list], mode:str = 'opex'):
    inputs = {}
    category = data.get(mode)
    with ui.element('main').classes(
        'flex-1 h-screen flex items-start justify-center pt-20'
        ):
            with ui.card().classes(
                '''
                w-full max-w-md p-8 shadow-lg rounded-2xl gap-4
                bg-[#101923]/90 border border-[#1f2937] text-white
                '''
            ):
                with ui.column().classes('w-full gap-3') as container:
                    for key, label in category.items():
                        inputs[key] = ui.input(
                            label=label,
                            placeholder='Введите сумму'
                        ).classes('w-full')

                    ui.button(
                        'Подключить оператора',
                        on_click=submit
                    ).classes('mt-4 w-full')

                container.on('keydown.enter', lambda e: submit(inputs))