from backend.api.routers.widget.charts.network_cost_structure.chart import NetworkCostStructureChart
from backend.api.routers.widget.charts.summary_time_series.chart import SummaryTimeSeries


CHART_REGISTRY  = {
    "network_cost_structure": NetworkCostStructureChart,
    "summary_time_series": SummaryTimeSeries,
}