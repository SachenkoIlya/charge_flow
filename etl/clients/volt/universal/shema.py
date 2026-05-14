from pydantic import BaseModel, Field
from typing import Any
from datetime import datetime

class LocationModel(BaseModel):
    model_config = {
        "extra": "forbid"
    }
    id: str | int
    name: str | None = None
    address: str | None = None
    city: str | None = None
    latitude: float | None = None
    longitude: float | None = None

class ChargePointModel(BaseModel):
    model_config = {
        "extra": "forbid"
    }
    id: str | int
    key: str
    name: str | None = None
    serialNumber: str | None = None
    state: str | None = None
    connected: bool | None = None
    lastSeen: str | None = None
    model: str | None = None
    vendor: str | None = None
    protocol: str | None = None
    operatorId: str | int | None = None
    operatorName: str | None = None
    location: LocationModel


class ChargingSessionModel(BaseModel):
    model_config = {
        "extra": "forbid"
    }
    session_id: str | int = Field(alias="id")
    charger_name: str | None = Field(default=None, alias="chargerName")
    evse_path: str | None = Field(default=None, alias="evsePath")
    connector_type: str | None = Field(default=None, alias="connectorType")
    evse_type: str | None = Field(default=None, alias="evseType")

    start_ts: datetime = Field(alias="startTs")
    end_ts: datetime | None = Field(default=None, alias="endTs")

    duration_minutes: float | None = Field(default=None, alias="durationMinutes")
    energy_kwh: float | None = Field(default=None, alias="energyKwh")
    soc_start: float | None = Field(default=None, alias="socStart")
    current_soc: float | None = Field(default=None, alias="currentSoc")
    charge_duration_minutes: float | None = Field(default=None, alias="chargeDurationMinutes")
    post_charge_duration_minutes: float | None = Field(default=None, alias="postChargeDurationMinutes")

    gross_revenue: float | None = Field(default=None, alias="grossRevenue")
    partner_revenue: float | None = Field(default=None, alias="partnerRevenue")
    subscriber_id: str | int | None = Field(default=None, alias="subscriberId")
    contract: str | None =  Field(default=None, alias="contract")
    state: str | None = Field(default=None, alias='state')
    reason: str | None = Field(default=None, alias='reason')