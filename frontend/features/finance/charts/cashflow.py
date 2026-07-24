from frontend.components.chart_card import chart_card
from nicegui import ui
from datetime import date, datetime
from typing import Any

MONTHS_RU = {
    1: "Янв",
    2: "Фев",
    3: "Мар",
    4: "Апр",
    5: "Май",
    6: "Июн",
    7: "Июл",
    8: "Авг",
    9: "Сен",
    10: "Окт",
    11: "Ноя",
    12: "Дек",
}


def render_cashflow_chart(cash_flow_history:list[dict]):
    if not cash_flow_history:
        ui.label("Нет данных для построения графика").classes(
            "text-gray-400 text-sm"
        ) 
        return
    
    options = prepare_data(cash_flow_history)
    with chart_card():
        ui.label('Накопленный денежный поток').classes('text-sm font-bold mb-2')
        ui.echart(options).classes('w-full h-[300px]')



def format_chart_date(value: str | date | datetime) -> str:
    if isinstance(value, datetime):
        parsed_date = value
    elif isinstance(value, date):
        parsed_date = value
    else:
        parsed_date = datetime.fromisoformat(value)

    return f"{MONTHS_RU[parsed_date.month]} {parsed_date.year}"



def prepare_data(cash_flow_history: list[dict[str, Any]]) -> dict:
    dates = [
        format_chart_date(item["date"])
        for item in cash_flow_history
    ]

    accumulated_values = [
        round(float(item["accumulated"]), 2)
        for item in cash_flow_history
    ]

    options = {
        "backgroundColor": "transparent",

        "title": {
            # "text": "Накопленный денежный поток",
            "left": 0,
            "top": 0,
            "textStyle": {
                "color": "#ffffff",
                "fontSize": 14,
                "fontWeight": 600,
            },
        },

        "tooltip": {
            "trigger": "axis",
            'triggerOn': 'click',
            "axisPointer": {
                "type": "line",
                 'snap': True,
                "lineStyle": {
                    "type": "dashed",
                    "color": "#94a3b8",
                },
            },
            ":valueFormatter": (
                "value => new Intl.NumberFormat('ru-RU', "
                "{minimumFractionDigits: 2, maximumFractionDigits: 2}"
                ").format(value)"
            ),
        },

        "grid": {
            'left': '3%',
            'right': '4%',
            'bottom': '3%',
            'containLabel': True
        },

        "xAxis": {
            "type": "category",
            "boundaryGap": True,
            "data": dates,
            "axisLine": {
                "lineStyle": {
                    "color": "#334155",
                },
            },
            "axisLabel": {
                "color": "#94a3b8",
            },
            "axisTick": {
                "show": False,
            },
        },

        "yAxis": {
            "type": "value",
            "axisLabel": {
                "color": "#94a3b8",
            },
            "axisLine": {
                "show": False,
            },
            "axisTick": {
                "show": False,
            },
            "splitLine": {
                "lineStyle": {
                    "color": "#1e293b",
                },
            },
        },

        "series": [
            {
                "name": "Накопленный поток",
                "type": "line",
                "smooth": True,
                "data": accumulated_values,
                "symbol": "circle",
                "symbolSize": 7,
                "showSymbol": True,

                "lineStyle": {
                    "width": 3,
                    "color": "#22c55e",
                },

                "itemStyle": {
                    "color": "#22c55e",
                    "borderColor": "#ffffff",
                    "borderWidth": 2,
                },

                "areaStyle": {
                    "color": {
                        "type": "linear",
                        "x": 0,
                        "y": 0,
                        "x2": 0,
                        "y2": 1,
                        "colorStops": [
                            {
                                "offset": 0,
                                "color": "rgba(34, 197, 94, 0.30)",
                            },
                            {
                                "offset": 1,
                                "color": "rgba(34, 197, 94, 0.02)",
                            },
                        ],
                    },
                },
            },
        ],
    }

    return options