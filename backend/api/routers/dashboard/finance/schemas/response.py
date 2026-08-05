from typing import Optional
from pydantic import BaseModel, Field
from datetime import date as dt, datetime   
from typing import Literal



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
    payback_period: float | None = Field(
        default=None,
        description="Расчётный срок окупаемости в месяцах. Может быть null, если расчёт невозможен.",
        examples=[58.0, None],
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
    operator_commission: Optional[float] = Field(
        description='Комиссия оператора за период'
    )
    
class InvestmentModel(BaseModel):
    capex: CapexModel = Field(
        description='Детализация всех капитальных затрат (CAPEX) по категориям.'
    )
    opex: OpexModel = Field(
        description='Детализация всех операционных расходов (OPEX) по категориям.'
    )

class NetworkCostStructureModel(BaseModel):
    electricity_compensation: float  = Field(
        description='Компенсация расходов на электроэнергию',
        examples=[165000.0]
    )
    rent_payment: float = Field(
        description='Расходы на аренду помещений или площадей',
        examples=[59000.0]
    )
    operator_commission: float  = Field(
        description='Комиссионное вознаграждение оператора',
        examples=[85000.0]
    )
    service_maintenance: float  = Field(
        description='Расходы на техническое и сервисное обслуживание',
        examples=[4000.0]
    )
    internet_and_connection: float = Field(
        description='Затраты на интернет, связь и каналы передачи данных',
        examples=[1150.0]
    )
    taxes: float  = Field(
        description='Налоговые отчисления и обязательные сборы',
        examples=[12000.0]
    )

class AccumulatedCashFlowModel(BaseModel):
    date: dt = Field(
        description="Дата начала отчётного периода.",
        examples=["2026-01-01"],
    )
    accumulated: float = Field(
        description=(
            "Накопленный чистый денежный поток с начала выбранного периода."
        ),
        examples=[847017.93],
    )
    net_cash_flow: float = Field(
        description=(
            "Чистый денежный поток за отчётный период: "
            "выручка владельца за вычетом операционных расходов."
        ),
        examples=[287002.38],
    )

class StationFinancialsModel(BaseModel):
    station_id: int = Field(
        description='Уникальный идентификатор зарядной станции.',
        examples=[137]
    )

    station_name: str = Field(
        description='Название или местоположение зарядной станции.',
        examples=['ТРЦ Станция 1']
    )

    revenue: float = Field(
        description='Общая выручка станции за выбранный период.',
        examples=[1830815.38]
    )

    electricity_cost: float = Field(
        description='Расходы на электроэнергию (компенсация электроэнергии) за выбранный период.',
        examples=[765672.26]
    )

    gross_profit: float = Field(
        description='Валовая прибыль: выручка за вычетом расходов на электроэнергию.',
        examples=[1065143.12]
    )

    opex: float = Field(
        description='Операционные расходы станции без учета электроэнергии и налогов (аренда, комиссия оператора, обслуживание, интернет, страхование и прочие расходы).',
        examples=[546681.53]
    )

    ebitda: float = Field(
        description='EBITDA станции — прибыль до вычета налогов после учета операционных расходов.',
        examples=[518461.59]
    )

    taxes: float = Field(
        description='Сумма налогов и обязательных сборов за выбранный период.',
        examples=[112871.96]
    )

    net_profit: float = Field(
        description='Чистая прибыль станции после вычета налогов.',
        examples=[405589.63]
    )

    net_margin: float = Field(
        description='Рентабельность по чистой прибыли, выраженная в процентах от выручки.',
        examples=[22.15]
    )
     



class WidgetsModel(BaseModel):
    # network_cost_structure: NetworkCostStructureModel = Field(
    #     description="Структура операционных расходов сети для построения графиков и диаграмм."
    # )

    # cash_flow_history: list[AccumulatedCashFlowModel] = Field(
    #     default_factory=list,
    #     description=(
    #         "История накопленного денежного потока. Каждый элемент содержит "
    #         "дату периода, чистый денежный поток за период и накопленное значение."
    #     ),
    #     examples=[
    #         [
    #             {
    #                 "date": "2026-01-01",
    #                 "net_cash_flow": 91243.41,
    #                 "accumulated": 91243.41,
    #             },
    #             {
    #                 "date": "2026-02-01",
    #                 "net_cash_flow": 80492.00,
    #                 "accumulated": 171735.41,
    #             },
    #         ]
    #     ],
    # )

    station_financials: list[StationFinancialsModel] = Field(
        default_factory=list,
        description='',
        examples=[
            [
                {
                    "station_id": 137,
                    "station_name": "ТРЦ Станция 1",
                    "revenue": 1830815.38,
                    "electricity_cost": 765672.26,
                    "gross_profit": 1065143.12,
                    "opex": 546681.53,
                    "ebitda": 518461.59,
                    "taxes": 112871.96,
                    "net_profit": 405589.63,
                    "margin": 22.15
                },
                {
                    "station_id": 138,
                    "station_name": "ТРЦ Станция 2",
                    "revenue": 1570152.54,
                    "electricity_cost": 636581.25,
                    "gross_profit": 933571.29,
                    "opex": 430515.41,
                    "ebitda": 503055.88,
                    "taxes": 94209.14,
                    "net_profit": 408846.74,
                    "margin": 26.04
                },
                {
                    "station_id": 139,
                    "station_name": "ТЦ Станция 3",
                    "revenue": 859755.72,
                    "electricity_cost": 346953.22,
                    "gross_profit": 512802.5,
                    "opex": 273625.61,
                    "ebitda": 239176.89,
                    "taxes": 51585.34,
                    "net_profit": 187591.55,
                    "margin": 21.82
                }
            ]
        ]
    )
class DateRangeModel(BaseModel):
    period: Literal["6m", "1y", "all"] = Field(
        description="Выбранный временной диапазон.",
        examples=["1y"],
    )
    date_from: datetime | None = Field(
        default=None,
        description=(
            "Начало выбранного временного диапазона. "
            "Для периода 'all' может быть null."
        ),
        examples=["2025-07-21T14:35:52", None],
    )
    date_to: datetime | None = Field(
        default=None,
        description=(
            "Конец выбранного временного диапазона. "
            "Для периода 'all' может быть null."
        ),
        examples=["2026-07-21T14:35:52", None],
    )

class FinanceResponseModel(BaseModel):
    metrics: MetricsModel = Field(
        description='Основные финансовые показатели бизнеса (выручка, EBITDA, чистая прибыль, денежный поток) за указанный период.'
    )
    investment: InvestmentModel = Field(
        description='Детализация инвестиционных расходов, сгруппированная по категориям CAPEX и OPEX.'
    )
    widgets: WidgetsModel = Field(
        description='Набор структурированных данных для визуализации аналитических графиков и диаграмм'
    )

    date_range: DateRangeModel = Field(
            description='Временной диапазон, за который были рассчитаны все финансовые метрики в ответе.'
        )
        
