from pydantic import BaseModel, Field
from typing import Optional

class PeriodSchema(BaseModel):
    date_from: Optional[str] = Field(
        description="Дата начала периода"
    )
    date_to: Optional[str] = Field(
        description="Дата окончания периода"
    )

class MetricsModel(BaseModel):
    total_sessions: Optional[float] = Field(
        description="Общее количество зарядных сессий"
    )
    total_revenue: Optional[float] = Field(
        description="Общая выручка за период"
    )
    avg_revenue_per_station: Optional[float] = Field(
        description="Средняя выручка на станцию"
    )
    avg_revenue_per_session: Optional[float] = Field(
        description="Средняя выручка на одну сессию"
    )
    total_energy_kwh: Optional[float] = Field(
        description="Общий объём отпущенной энергии, кВт⋅ч"
    )

class StationModel(BaseModel):
    total_station: Optional[int]
    connected_stations: Optional[int]

class MarginModel(BaseModel):
    partner_revenue: Optional[float] = Field(
        description="Доход владельца станции"
    )
    partner_pct: Optional[float] = Field(
        description="Доля владельца станции в процентах"
    )
    operator_revenue: Optional[float] = Field(
        description="Доход оператора ChargeFlow"
    )
    operator_pct: Optional[float] = Field(
        description="Доля оператора в процентах"
    )
class SeriesChartsModel(BaseModel):
    revenue: Optional[list[float]] = Field(
        default=None,
        description="Массив значений выручки по периодам"
    )
    sessions: Optional[list[int]] = Field(
        default=None,
        description="Массив количества зарядных сессий по периодам"
    )
    utilisation: Optional[list[float]] = Field(
        default=None,
        description="Массив значений загрузки сети в процентах по периодам"
    )
class ChartsModel(BaseModel):
    xAxis: Optional[list[str]] = Field(
        default=None,
        description="Подписи временной оси графика (дни, недели или месяцы)"
    )
    series: SeriesChartsModel = Field(
        description="Набор временных рядов для построения графиков"
    )

class StationRatingBlockModel(BaseModel):
    station_id: Optional[int] = Field(
        description="Идентификатор станции"
    )
    station_name: Optional[str] = Field(
        description="Название или локация станции"
    )
    revenue: Optional[float] = Field(
        description="Выручка станции за период"
    )
    utilisation: Optional[float] = Field(
        description="Средняя загрузка станции в процентах"
    )

class StationRatingModel(BaseModel):
    top_stations: list[StationRatingBlockModel] = Field(
        default_factory=list,
        description="Топ-5 станций по выручке за выбранный период"
    )
    worst_stations: list[StationRatingBlockModel] = Field(
        default_factory=list,
        description="5 станций с наименьшей выручкой за выбранный период"
    )

class MetricsBlockModel(BaseModel):
    metrics: MetricsModel = Field(
        description="Основные финансовые и эксплуатационные показатели"
    )
    station: StationModel = Field(
        description="Статистика подключённых станций"
    )
    utilisation: Optional[float] = Field(
        default=None,
        description="Средняя загрузка сети в процентах"
    )
    margin: Optional[MarginModel] = Field(
        default=None,
        description="Распределение выручки между партнёром и оператором"
    )
    charts: Optional[ChartsModel] = Field(
        default=None,
        description="Данные для построения графиков"
    )
    station_rating: Optional[StationRatingModel] = Field(
        default=None,
        description="Рейтинг лучших и худших станций"
    )


class SummaryResponseModel(BaseModel):
    requested_metrics: MetricsBlockModel = Field(
        description="Метрики и аналитика за выбранный период"
    )

    comparable_metrics: MetricsBlockModel = Field(
        description="Метрики и аналитика за предыдущий сопоставимый период"
    )

    requested_period: PeriodSchema = Field(
        description="Границы анализируемого периода"
    )

    comparable_period: PeriodSchema = Field(
        description="Границы периода сравнения"
    )