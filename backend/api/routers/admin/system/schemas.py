from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class MonitoringMode(str, Enum):
    etl_run = "etl_run"
    bi_exports = "bi_exports"

class SystemSchema(BaseModel):
    mode: MonitoringMode


class MonitoringSchema(BaseModel):
    user_id: int = Field(
        description="Идентификатор пользователя"
    )
    type_method: str = Field(
        description="Тип выполняемого процесса"
    )
    run_mode: str = Field(
        description="Режим запуска процесса"
    )
    operator: str = Field(
        description="Источник запуска процесса"
    )
    status: str = Field(
        description="Текущий статус выполнения"
    )
    last_success_at: datetime | None = Field(
        default=None,
        description="Время последнего успешного запуска"
    )
    created_at: datetime | None = Field(
        default=None,
        description="Время создания задачи"
    )
    run_id: str | None = Field(
        default=None,
        description="Уникальный идентификатор запуска"
    )
    error: str | None = Field(
        default=None,
        description="Текст ошибки при неуспешном выполнении"
    )
    updated_at: datetime | None = Field(
        default=None,
        description="Время последнего обновления записи"
    )
    processed_at: datetime | None = Field(
        default=None,
        description="Время завершения обработки"
    )
    

class EtlRunsResponseSchema(BaseModel):
    rows: list[MonitoringSchema] = Field(
        description="Список запусков процессов мониторинга"
    )