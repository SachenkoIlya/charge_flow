from datetime import datetime
from core.logger.logger import logger
from dateutil.relativedelta import relativedelta

def get_period_days(
    date_from:datetime, 
    date_to:datetime
) -> str:
    """
    Определяет уровень агрегации данных в зависимости от длительности периода.
    Используется для выбора оптимального интервала группировки
    временных рядов при построении отчётов и графиков.
    Правила выбора:
        - до 90 дней включительно — группировка по дням (`day`);
        - от 91 до 365 дней включительно — группировка по неделям (`week`);
        - более 365 дней — группировка по месяцам (`month`).
    Args:
        date_from (datetime): Начало периода.
        date_to (datetime): Конец периода.
    Returns:
        str:
            Тип группировки:
            - `day` — по дням;
            - `week` — по неделям;
            - `month` — по месяцам.
    Example:
        >>> get_period_days(
        ...     datetime(2025, 1, 1),
        ...     datetime(2025, 3, 1)
        ... )
        'day'
        >>> get_period_days(
        ...     datetime(2025, 1, 1),
        ...     datetime(2025, 10, 1)
        ... )
        'week'
        >>> get_period_days(
        ...     datetime(2024, 1, 1),
        ...     datetime(2026, 1, 1)
        ... )
        'month'
    """
    period_days = (date_to - date_from).days
    if period_days <= 90:
        group_by = 'day'
    elif period_days <= 365:
        group_by = 'week'
    else:
        group_by = 'month'
    return group_by


def get_date_expr(group_by: str) -> str:
    """
    Возвращает SQL-выражение для группировки данных по временному периоду.

    Используется при формировании аналитических запросов для агрегации
    данных по дням, неделям или месяцам.

    Args:
        group_by (str): Тип группировки (`day`, `week`, `month`).

    Returns:
        str: SQL-выражение для группировки по выбранному периоду.

    Raises:
        ValueError: Если передан неподдерживаемый тип группировки.
    """
    mapping = {
        "day": "DATE(cs.start_ts)",
        "week": "DATE_TRUNC('week', cs.start_ts)",
        "month": "DATE_TRUNC('month', cs.start_ts)",
    }
    try:
        return mapping[group_by]
    except KeyError:
        raise ValueError("invalid group_by")


def comparable_period(
    date_from:datetime, 
    date_to:datetime
) -> tuple[datetime, datetime]:
        """
        Вычисляет предыдущий период аналогичной продолжительности.

        Используется для сравнительного анализа текущего периода
        с предыдущим периодом такой же длины.

        Args:
            date_from (datetime): Начало текущего периода.
            date_to (datetime): Конец текущего периода.

        Returns:
            tuple[datetime, datetime]:
                Кортеж из дат:

                - comparable_from — начало предыдущего периода;
                - comparable_to — конец предыдущего периода
                (совпадает с началом текущего периода).

        Example:
            Текущий период:
                2025-02-01 → 2025-03-01

            Результат:
                2025-01-04 → 2025-02-01
        """
        is_full_month = (
            date_from.day == 1
            and date_to.day == 1
            and date_to == date_from + relativedelta(months=1)
        )

        if is_full_month:
            comparable_from = date_from - relativedelta(months=1)
            comparable_to = date_from
        else:
            period = date_to - date_from
            comparable_to = date_from
            comparable_from = comparable_to - period

        return comparable_from, comparable_to
    
    
def _calc_utilisation(
    charging_minutes: float, 
    evse_count: float, 
    date_from:datetime, 
    date_to:datetime
) -> float:
    period_minutes = (date_to - date_from).total_seconds() / 60
    available_minutes = (evse_count * period_minutes)
    if available_minutes == 0:
        return 0
    return round(
        charging_minutes / available_minutes * 100, 
        2
    )