from typing import Optional
from pydantic import BaseModel, Field


class FinanceFilterSchema(BaseModel):
    toggle_value: Optional[str] = Field(
        description=(
            "Период отчета. Возможные значения: "
            "'6m' (6 месяцев), "
            "'1y' (1 год), "
            "'all' (весь период). "
        ),
        examples=['all'],
    )

class MetricsModel(BaseModel):
    total_revenue: Optional[float] = Field(
        description='Общая выручка компании за выбранный период (сумма всех доходов от продаж).'
    )
    ebitda: Optional[float] = Field(
        description='Прибыль до вычета процентов, налогов и амортизации. Рассчитывается как: Выручка - Операционные расходы (без налогов).'
    )
    net_profit: Optional[float] = Field(
        description='Чистая прибыль. Итоговый финансовый результат компании после вычета всех операционных расходов и налогов.'
    )
    cash_flow: Optional[float] = Field(
        description='Денежный поток (Cash Flow). Реальный остаток свободных денег на счетах после вычета всех операционных и капитальных затрат.'
    )
    payback_period: Optional[float] = Field(
        description='Срок окупаемости инвестиций в месяцах. Рассчитывается как отношение общего CAPEX к среднемесячной чистой прибыли.'
    )

class CapexModel(BaseModel):
    construction_and_installation: Optional[float] = Field(
        description='Затраты на строительно-монтажные работы, ремонт и обустройство объектов.'
    )
    other_capex: Optional[float] = Field(
        description='Прочие капитальные вложения и крупные разовые инвестиции.'
    )
    location_search: Optional[float] = Field(
        description='Расходы на поиск, подбор и юридическую проверку новых локаций или недвижимости.'
    )
    equipment_purchase: Optional[float] = Field(
        description='Затраты на покупку производственного, торгового или офисного оборудования.'
    )

class OpexModel(BaseModel):
    insurance: Optional[float] = Field(
        description='Расходы на страхование имущества, бизнеса или рисков.'
    )
    taxes: Optional[float] = Field(
        description='Сумма выплаченных налогов и обязательных сборов.'
    )
    service_maintenance: Optional[float] = Field(
        description='Затраты на техническое и сервисное обслуживание оборудования или объектов.'
    )
    internet_and_connection: Optional[float] = Field(
        description='Расходы на интернет, телефонию и прочие услуги связи.'
    )
    rent_payment: Optional[float] = Field(
        description='Арендные платежи за помещения, землю или технику.'
    )
    other_expenses: Optional[float] = Field(
        description='Прочие текущие операционные расходы, не вошедшие в основные категории.'
    )
    electricity_compensation: Optional[float] = Field(
        description='Расходы на оплату электроэнергии или компенсацию коммунальных услуг.'
    )

class InvestmentModel(BaseModel):
    capex: CapexModel = Field(
        description='Детализация всех капитальных затрат (CAPEX) по категориям.'
    )
    opex: OpexModel = Field(
        description='Детализация всех операционных расходов (OPEX) по категориям.'
    )

class NetworkCostStructureModel(BaseModel):
    electricity_compensation: Optional[float | int] = Field(
        description='Компенсация расходов на электроэнергию',
        examples=[165000.0]
    )
    rent_payment: Optional[float | int] = Field(
        description='Расходы на аренду помещений или площадей',
        examples=[59000.0]
    )
    operator_commission: Optional[float | int] = Field(
        description='Комиссионное вознаграждение оператора',
        examples=[85000.0]
    )
    service_maintenance: Optional[float | int] = Field(
        description='Расходы на техническое и сервисное обслуживание',
        examples=[4000.0]
    )
    internet_and_connection: Optional[float | int] = Field(
        description='Затраты на интернет, связь и каналы передачи данных',
        examples=[1150.0]
    )
    taxes: Optional[float | int] = Field(
        description='Налоговые отчисления и обязательные сборы',
        examples=[12000.0]
    )


class ChartsModel(BaseModel):
    network_cost_structure: NetworkCostStructureModel = Field(
        description='Структура операционных расходов сети для построения графиков и диаграмм'
    )

class DateRangeModel(BaseModel):
    period: Optional[str] = Field(
        examples=["1y", '6m', 'all'],
        description='Идентификатор выбранного временного диапазона для фильтрации данных.'
    )
    date_from: Optional[str | None] = Field(
        examples=['2025-07-21 14:35:52', None],
        description='Начальная дата и время периода в формате YYYY-MM-DD HH:MM:SS. Может быть null, если данных нет.'
    )
    date_to: Optional[str | None] = Field(
        examples=['2026-07-21 14:35:52', None],
        description='Конечная дата и время периода в формате YYYY-MM-DD HH:MM:SS. Может быть null, если данных нет.'
    )

class FinanceResponseModel(BaseModel):
    metrics: MetricsModel = Field(
        description='Основные финансовые показатели бизнеса (выручка, EBITDA, чистая прибыль, денежный поток) за указанный период.'
    )
    investment: InvestmentModel = Field(
        description='Детализация инвестиционных расходов, сгруппированная по категориям CAPEX и OPEX.'
    )
    date_range: DateRangeModel = Field(
        description='Временной диапазон, за который были рассчитаны все финансовые метрики в ответе.'
    )
    charts: ChartsModel = Field(
        description='Набор структурированных данных для визуализации аналитических графиков и диаграмм'
    )
        
