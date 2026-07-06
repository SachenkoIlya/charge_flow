from pydantic import BaseModel, Field
from typing import Literal

class ResponseModel(BaseModel):
    """Универсальная схема успешного ответа API на запросы модификации данных.
    
    Возвращается после успешного сохранения, обновления или удаления записей.
    """
    success: bool = Field(
        description='Флаг успешности выполнения операции (True — успешно, False — произошла ошибка)',
        examples=[True]
    )
    message: str = Field(
        description='Текстовое уведомление для пользователя или логов о результате операции',
        examples=['Данные успешно сохранены']
    )


# class InvestmentExpenseCreateSchema(BaseModel):
#     mode: Literal['capex', 'opex']

#     station_id: int
#     expense_date: str | None = None
#     # CAPEX
#     location_search: float | None = None
#     equipment_purchase: float | None = None
#     construction_and_installation: float | None = None
#     other_capex: float | None = None

#     # OPEX
#     electricity_compensation: float | None = None
#     rent_payment: float | None = None
#     operator_commission: float | None = None
#     internet_and_connection: float | None = None
#     taxes: float | None = None
#     insurance: float | None = None
#     service_maintenance: float | None = None
#     other_expenses: float | None = None

#     comment: str | None = None

class InvestmentExpenseCreateSchema(BaseModel):
    """Схема для создания записи о финансовых вложениях или операционных расходах.
    
    Используется для отправки данных из форм CAPEX и OPEX. Позволяет
    фиксировать траты по конкретной станции.
    """
    
    mode: Literal['capex', 'opex'] = Field(
        description="Режим записи: 'capex' (капитальные затраты) или 'opex' (операционные расходы)"
    )
    station_id: int = Field(
        description="Уникальный идентификатор станции, к которой относятся расходы"
    )
    expense_date: str | None = Field(
        default=None,
        description="Дата совершения расхода/инвестиции (например, в формате 'YYYY-MM-DD')"
    )

    # Блок CAPEX (Капитальные затраты) 
    location_search: float | None = Field(
        default=None,
        description="[CAPEX] Затраты на поиск, подбор и аудит локации"
    )
    equipment_purchase: float | None = Field(
        default=None,
        description="[CAPEX] Расходы на покупку основного и вспомогательного оборудования"
    )
    construction_and_installation: float | None = Field(
        default=None,
        description="[CAPEX] Стоимость строительно-монтажных и пусконаладочных работ (СМР)"
    )
    other_capex: float | None = Field(
        default=None,
        description="[CAPEX] Прочие единовременные капитальные вложения"
    )

    # Блок OPEX (Операционные расходы) 
    electricity_compensation: float | None = Field(
        default=None,
        description="[OPEX] Компенсация или оплата расходов за электроэнергию"
    )
    rent_payment: float | None = Field(
        default=None,
        description="[OPEX] Арендные платежи за размещение оборудования/станции"
    )
    operator_commission: float | None = Field(
        default=None,
        description="[OPEX] Комиссия оператора или платежного сервиса"
    )
    internet_and_connection: float | None = Field(
        default=None,
        description="[OPEX] Расходы на интернет, сотовую связь и каналы коммуникации"
    )
    taxes: float | None = Field(
        default=None,
        description="[OPEX] Налоговые отчисления и сборы"
    )
    insurance: float | None = Field(
        default=None,
        description="[OPEX] Расходы на страхование оборудования и рисков"
    )
    service_maintenance: float | None = Field(
        default=None,
        description="[OPEX] Регулярное сервисное и техническое обслуживание (ТО)"
    )
    other_expenses: float | None = Field(
        default=None,
        description="[OPEX] Прочие регулярные операционные издержки"
    )

    comment: str | None = Field(
        default=None,
        description="Произвольный комментарий или примечание к финансовой записи"
    )