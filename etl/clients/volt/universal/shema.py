from pydantic import BaseModel, Field
from typing import Any
from datetime import datetime


class LocationModel(BaseModel):
    model_config = {
        "extra": "forbid"
    }
    id: str | int = Field(
        description="Уникальный идентификатор локации во внешней системе"
    )
    name: str | None = Field(
        default=None, 
        description="Коммерческое или понятное название локации"
    )
    address: str | None = Field(
        default=None, 
        description="Физ. адрес (улица, дом, строение)"
    )
    city: str | None = Field(
        default=None, 
        description="Город или населенный пункт"
    )
    latitude: float | None = Field(
        default=None, 
        description="Географическая широта (latitude) локации"
    )
    longitude: float | None = Field(
        default=None, 
        description="Географическая долгота (longitude) локации"
    )

class ChargePointModel(BaseModel):
    model_config = {
        "extra": "forbid"
    }
    id: str | int = Field(
        description="Уникальный идентификатор зарядной станции во внешней системе"
    )
    key: str = Field(
        description="Уникальный строковый ключ / токен авторизации терминала"
    )
    name: str | None = Field(
        default=None, 
        description="Отображаемое имя зарядной станции в интерфейсе"
    )
    serialNumber: str | None = Field(
        default=None, 
        description="Заводской серийный номер оборудования"
    )
    state: str | None = Field(
        default=None, 
        description="Текущий статус работы (например: Available, Charging, Faulted)"
    )
    connected: bool | None = Field(
        default=None, 
        description="Статус сетевого соединения (true — онлайн, false — оффлайн)"
    )
    lastSeen: str | None = Field(
        default=None, 
        description="Дата и время последнего сеанса связи в формате ISO 8601"
    )
    model: str | None = Field(
        default=None, 
        description="Заводская модель зарядного устройства"
    )
    vendor: str | None = Field(
        default=None, 
        description="Наименование производителя (бренд оборудования)"
    )
    protocol: str | None = Field(
        default=None, 
        description="Версия поддерживаемого протокола OCPP"
    )
    operatorId: str | int | None = Field(
        default=None, 
        description="Идентификатор оператора ЭЗС (владельца сети)"
    )
    operatorName: str | None = Field(
        default=None, 
        description="Наименование компании-оператора"
    )
    location: LocationModel = Field(
        description="Данные о географическом местоположении станции"
    )



class ChargingSessionModel(BaseModel):
    model_config = {
        "extra": "forbid"
    }
    session_id: str | int = Field(
        alias="id",
        description="Уникальный идентификатор сессии зарядки во внешней системе"
    )
    charger_name: str | None = Field(
        default=None, 
        alias="chargerName",
        description="Название или коммерческое имя зарядной станции"
    )
    evse_path: str | None = Field(
        default=None, 
        alias="evsePath",
        description="Путь или уникальный индекс порта/точки подключения (EVSE ID)"
    )
    connector_type: str | None = Field(
        default=None, 
        alias="connectorType",
        description="Тип зарядного разъема (например: Type 2, CCS Combo 2, CHAdeMO)"
    )
    evse_type: str | None = Field(
        default=None, 
        alias="evseType",
        description="Тип тока станции (например: AC — переменный, DC — постоянный)"
    )

    start_ts: datetime = Field(
        alias="startTs",
        description="Дата и время начала сессии зарядки"
    )
    end_ts: datetime | None = Field(
        default=None, 
        alias="endTs",
        description="Дата и время фактического или планового завершения сессии"
    )

    duration_minutes: float | None = Field(
        default=None, 
        alias="durationMinutes",
        description="Общая длительность сессии с момента подключения в минутах"
    )
    energy_kwh: float | None = Field(
        default=None, 
        alias="energyKwh",
        description="Количество потребленной/переданной электроэнергии в кВт⋅ч"
    )
    soc_start: float | None = Field(
        default=None, 
        alias="socStart",
        description="Уровень заряда батареи электромобиля (SoC) в начале сессии в %"
    )
    current_soc: float | None = Field(
        default=None, 
        alias="currentSoc",
        description="Текущий или финальный уровень заряда батареи (SoC) в %"
    )
    charge_duration_minutes: float | None = Field(
        default=None, 
        alias="chargeDurationMinutes",
        description="Чистое время активной подачи тока/зарядки в минутах"
    )
    post_charge_duration_minutes: float | None = Field(
        default=None, 
        alias="postChargeDurationMinutes",
        description="Время простоя после окончания зарядки (машина подключена, но не заряжается) в минутах"
    )

    gross_revenue: float | None = Field(
        default=None, 
        alias="grossRevenue",
        description="Общая сумма выручки за сессию (грязный доход)"
    )
    partner_revenue: float | None = Field(
        default=None, 
        alias="partnerRevenue",
        description="Доля выручки, причитающаяся партнеру/владельцу локации"
    )
    subscriber_id: str | int | None = Field(
        default=None, 
        alias="subscriberId",
        description="Идентификатор пользователя (подписчика), запустившего зарядку"
    )
    contract: str | None = Field(
        default=None, 
        alias="contract",
        description="Номер договора, контракта или платежного соглашения"
    )
    state: str | None = Field(
        default=None, 
        alias='state',
        description="Текущий статус сессии (например: Active, Completed, Canceled)"
    )
    reason: str | None = Field(
        default=None, 
        alias='reason',
        description="Причина завершения сессии (например: LocalStop, RemoteStop, EVDisconnected)"
    )