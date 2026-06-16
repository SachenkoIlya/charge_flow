from nicegui import ui
from core.logger.logger import logger
from datetime import datetime
from frontend.features.investments_and_expenses.schemas.schemas import (
    resolve_model, 
    CapexSchema, 
    OpexSchema
)
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

def build_paylaod(
    mode:str, 
    comment_input, 
    model: CapexSchema | OpexSchema
):
    model.comment = comment_input.value
    payload = model.model_dump()
    payload['mode'] = mode
    return payload


async def final_submit(
    payload: dict,
    request: Request, 
    endpoint_name: str ='investments'
):
    response = await frontend_api(
        request=request,
        endpoint_name=endpoint_name,
        payloads=payload
    )
    if response is None:
        return None
    return response
    

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


def resolve_expense_fields(payload: dict):
    expense_fields = [
        key for key in payload.keys()
        if key not in ('station_id', 'comment', 'expense_date')
    ]
    has_values = any(
        payload.get(field) not in (None, '', 0, '0')
        for field in expense_fields
    )
    return has_values




async def render_form(data: dict[str, list], request: Request, mode:str = 'opex'):
    inputs = {}
    category = data.get(mode)

    selected_station = await get_selected_station(request=request)

    async def submit():
        payload = {
            key: (
                None if input_.value == '' else input_.value
            )
            for key, input_ in inputs.items()
        }
        if payload.get('station_id') is None:
            ui.notify(
                'Выберите станцию',
                color='red'
            )
            return
        
        has_value = resolve_expense_fields(payload)
        if not has_value:
            ui.notify(
                'Минимум одно поле должно быть заполнено',
                color='orange',
                position='top',
            )
            return
        
        model = resolve_model(payload, mode)
        
        if not model:
            return 
        
        station_label = selected_station.get(str(model.station_id))

        with ui.dialog() as dialog, ui.card().classes('bg-[#101923] text-white w-[720px] max-w-[90vw] p-6'):
            ui.label('Подтвердите данные').classes('text-xl font-bold')

            ui.separator()
            ui.label(f'Станция: {station_label}')
            ui.label(f'Тип расходов: {mode.upper()}')

            for key, value in model.model_dump().items():
                if key in ('station_id', 'comment'):
                    continue
                label = category.get(key, key)
                if value:
                    ui.label(f'{label}: {value}')
            
            comment_input = ui.textarea(
                label='Комментарий',
                placeholder='Необязательный комментарий'
            ).props(
                'filled counter max_length=150'
            ).classes('w-full')
            
            async def on_confirm():
                allowed_payload = build_paylaod(
                    mode=mode,
                    comment_input=comment_input,
                    model=model
                )

                response = await final_submit(
                    payload=allowed_payload,
                    request=request 
                )
                if response is None:
                    return
                
                dialog.close()

                ui.notify(
                    response.get('message', 'Успешно сохранено'),
                    color='positive'
                )
                ui.navigate.reload()
            
            
            with ui.row().classes('w-full justify-end gap-3 mt-4'):
                ui.button('Отмена', on_click=dialog.close).props('flat')
                ui.button(
                    'Подтвердить',
                    on_click=on_confirm
                ).classes('bg-green-600 text-white')
            dialog.open()

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


                # inputs['expense_date'] = ui.input(
                #     label='Дата расхода',
                #     value=datetime.now().strftime('%d.%m.%Y'),
                # ).props('dense mask=##.##.####').classes('w-full')

                # with inputs['expense_date'].add_slot('append'):
                #     with ui.element('q-icon').props('name=event').classes('cursor-pointer'):
                #         with ui.element('q-popup-proxy').props(
                #             'cover transition-show=scale transition-hide=scale'
                #         ) as popup:
                #             ui.date(
                #                 value=datetime.now().strftime('%Y-%m-%d'),
                #                 on_change=lambda e: (
                #                     inputs['expense_date'].set_value(
                #                         datetime.strptime(e.value, '%Y-%m-%d').strftime('%d.%m.%Y')
                #                     ),
                #                     popup.run_method('hide'),
                #                 ),
                #             )
                with ui.input(label='Дата расхода').props('readonly') as date_input:
                    with ui.menu().props('no-parent-event') as menu:
                        ui.date().bind_value(date_input)

                date_input.on('click', menu.open)

                placeholder='Введите сумму'
                for key, label in category.items():
                    inputs[key] = ui.input(
                        label=label,
                        placeholder=placeholder
                        
                    ).classes(
                        'w-full'
                    ).props(
                        'dense'
                    )

                ui.button(
                    'Применить',
                    on_click=submit
                ).classes(
                    'mt-4 w-full'
                )