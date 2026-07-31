
from backend.api.routers.dashboard.finance.service.conext import PeriodContext
from backend.api.routers.dashboard.summary.db import SummaryDB
from backend.utils.calc_utilisation import _calc_utilisation


class Utilisation:
    def __init__(self, repository: "SummaryDB"):
        self.repository = repository

    async def calc_utilisation(self, ctx: PeriodContext):
        """
        Рассчитывает коэффициент утилизации (Utilisation Rate) зарядных станций
        за указанный период.
        Утилизация показывает, какой процент доступного времени зарядные
        станции фактически использовались для зарядки.
        Формула расчёта:
            utilisation = charging_minutes /
                          (evse_count * period_minutes) * 100
        где:
            - charging_minutes — суммарное время зарядки за период в минутах;
            - evse_count — количество доступных EVSE;
            - period_minutes — длительность периода в минутах.
        Args:
            user_id: Идентификатор пользователя.
            date_from (datetime): Начало периода расчёта.
            date_to (datetime): Конец периода расчёта.
        Returns:
            float:
                Процент утилизации зарядной инфраструктуры,
                округлённый до двух знаков после запятой.
                Возвращает 0, если количество доступных минут равно нулю.
        Example:
            Для периода в 24 часа (1440 минут),
            2 зарядных точек и 720 минут зарядки:
                available_minutes = 2 * 1440 = 2880
                utilisation = 720 / 2880 * 100 = 25.0
            Результат:
                25.0
        """
        rows = await self.repository.get_utilisation_metrics(
            user_id=ctx.user_id, 
            date_from=ctx.date_from, 
            date_to=ctx.date_to,
            station_ids=ctx.station_ids
        )
        return _calc_utilisation(
            charging_minutes=float(rows['charging_minutes']),
            evse_count=float(rows['evse_count']),
            date_from=ctx.date_from,
            date_to=ctx.date_to
        )