from datetime import datetime, timedelta    
from dateutil.relativedelta import relativedelta
from core.logger.logger import logger


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
        # Проверяем, охватывает ли выбранный диапазон ровно один полный календарный месяц
        # (Например: с 1 числа текущего месяца по 1 число следующего месяца)
        is_full_month = (
            date_from.day == 1
            and date_to.day == 1
            and date_to == date_from + relativedelta(months=1)
        )
        if is_full_month:
            # Если выбран ровно полный месяц, то прошлым периодом будет 
            # предыдущий календарный месяц (корректно учтет разное количество дней: 28, 30, 31)
            comparable_from = date_from - relativedelta(months=1)
            comparable_to = date_from
        else:
            # Если выбран произвольный период (например, 14 дней или полгода), 
            # то вычисляем его точную продолжительность в днях/часах
            period = date_to - date_from
            # Конечной точкой прошлого периода становится начало текущего периода
            comparable_to = date_from
            # Сдвигаем начальную точку прошлого периода назад на точно такую же длительность
            comparable_from = comparable_to - period
        # Возвращаем границы дат для аналогичного прошлого периода для расчета динамики (Delta)
        return comparable_from, comparable_to
    



def get_last_30_days_with_comparable_period() -> dict[str, tuple[datetime]]:
    requested_to = datetime.now()
    requested_from = requested_to - timedelta(days=30)
    comparable_to = requested_from
    comparable_from = comparable_to - timedelta(days=30)
    return {
        'requested': (requested_from, requested_to),
        'comparable': (comparable_from,comparable_to)
    }

def get_date_range_from_period(period: str) -> tuple[datetime|None, datetime|None]:
    """Вычисляет диапазон дат (начало и конец) на основе переданного текстового периода.

    Используется для фильтрации финансовых метрик на дашборде за определенный 
    промежуток времени относительно текущего момента.

    Args:
        period: Строковый идентификатор периода. Допустимые значения:
            - 'all': за всё время.
            - '6m': за последние 6 месяцев.
            - '1y': за последний 1 год.

    Returns:
        tuple[datetime | None, datetime | None]: Кортеж из двух элементов (date_from, date_to).
            Если выбран период 'all', возвращает (None, None), что означает отсутствие фильтра.

    Raises:
        ValueError: Если передан неизвестный или неподдерживаемый строковый период.
    """
    
    if period is None:
        raise ValueError("Period value is missing in the payload")
    # Фиксируем текущую дату и время как конечную точку диапазона
    date_to = datetime.now()
    # Обрабатываем выборку за всё время (границы дат не ограничиваются)
    if period == 'all':
        return None, None
    # Вычитаем 6 месяцев от текущей даты
    if period == '6m':
        return date_to - relativedelta(months=6), date_to
    # Вычитаем 1 год от текущей даты
    if period == '1y':
       return date_to - relativedelta(years=1), date_to
     # Возбуждаем исключение, если фронтенд прислал некорректный toggle
    raise ValueError(f'Unknown toggle value: {period}')
