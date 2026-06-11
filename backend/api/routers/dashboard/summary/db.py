from core.base_db import Base
from datetime import datetime   
from asyncpg import Record

class SummaryDB:
    """
    Слой доступа к данным аналитики и агрегированных метрик.
    Выполняет запросы к базе данных для формирования показателей
    и статистики зарядной инфраструктуры.
    """
    def  __init__(self, base_db: "Base"):
        self.db = base_db
    
 
    async def ping(self, user_id: int) -> int:
        """
        Проверяет наличие данных по пользователю в таблице зарядных сессий.

        Метод подсчитывает количество записей в таблице
        `charging_sessions_fact`, связанных с указанным пользователем.

        Может использоваться для проверки доступности данных перед
        выполнением более ресурсоёмких аналитических запросов.

        Args:
            user_id (int): Идентификатор пользователя.

        Returns:
            int:
                Количество найденных записей зарядных сессий.

                - 0 — данные отсутствуют;
                - > 0 — данные пользователя присутствуют.

        Example:
            >>> await repository.ping(123)
            1542

        Notes:
            Метод использует `fetchval()`, поэтому возвращает одно
            числовое значение, а не запись (`Record`).
        """
        q = """
            SELECT COUNT(*) 
            FROM charging_sessions_fact 
            WHERE user_id = $1
            """
        async with self.db.pool.acquire() as conn:
            return await conn.fetchval(q, user_id)
        
    async def get_charts(
        self, 
        user_id: int, 
        date_from: datetime, 
        date_to: datetime, 
        date_expr: str
    ) -> list[Record]:
        """
        Получает агрегированные данные для построения графиков за указанный период.

        Метод группирует зарядные сессии по переданному временному выражению
        (`date_expr`) и возвращает показатели по каждому периоду.

        Args:
            user_id (int): Идентификатор пользователя.
            date_from (datetime): Начало периода выборки (включительно).
            date_to (datetime): Конец периода выборки (не включительно).
            date_expr (str): SQL-выражение для группировки по периоду,
                например день, неделя или месяц.

        Returns:
            list[asyncpg.Record]:
                Список записей с агрегированными данными по периодам:

                - period — период группировки;
                - evse_count (int) — общее количество уникальных EVSE;
                - sessions (int) — количество зарядных сессий за период;
                - revenue (numeric) — выручка по завершённым сессиям;
                - charging_minutes (numeric) — длительность завершённых зарядок в минутах.

        Notes:
            - Метод использует `fetch()`, поэтому возвращает список записей.
            - Если данных за период нет, вернётся пустой список.
            - В расчёт `revenue` и `charging_minutes` включаются только
            сессии со статусом `COMPLETED`.
        """
        q = f"""
            WITH evse_total AS (
                SELECT
                    COUNT(DISTINCT cs.evse_path) AS evse_count
                FROM charging_sessions_fact cs
                WHERE cs.user_id = $1
            )
            SELECT
                {date_expr} as period
                ,
                (SELECT evse_count FROM evse_total) AS evse_count
                ,
                COUNT(*) AS sessions
                ,
                COALESCE(
                    SUM(cs.gross_revenue)
                        FILTER(WHERE cs.state = 'COMPLETED'),
                        0
                ) AS revenue
                ,
                COALESCE(
                    SUM(cs.charge_duration_minutes)
                        FILTER(WHERE cs.state = 'COMPLETED'),
                        0
                ) AS charging_minutes
            FROM charging_sessions_fact cs
            WHERE user_id = $1
                AND cs.start_ts >= $2
                AND cs.start_ts < $3 
            GROUP BY period
            ORDER BY period
            """
        async with self.db.pool.acquire() as conn:
            return await conn.fetch(q, user_id, date_from, date_to)

    async def get_metrics(self, user_id: int, date_from: datetime, date_to: datetime) -> Record | None:
        """
        Получает агрегированные операционные и финансовые показатели
        по зарядным сессиям за указанный период.

        Метод выполняет расчёт ключевых метрик на уровне базы данных,
        включая количество сессий, выручку и объём отпущенной энергии.

        Для финансовых и энергетических показателей учитываются только
        сессии со статусом `COMPLETED`.

        Рассчитываемые показатели:

        - общее количество сессий;
        - общая выручка;
        - средняя выручка на станцию;
        - средняя выручка на сессию;
        - общий объём отпущенной энергии.

        Args:
            user_id (int): Идентификатор пользователя.
            date_from (datetime): Начало периода выборки (включительно).
            date_to (datetime): Конец периода выборки (не включительно).

        Returns:
            asyncpg.Record:
                Запись с агрегированными показателями:

                - total_sessions (int) — общее количество зарядных сессий;
                - total_revenue (numeric) — суммарная выручка по завершённым сессиям;
                - avg_revenue_per_station (numeric) — средняя выручка на одну уникальную станцию;
                - avg_revenue_per_session (numeric) — средняя выручка на одну завершённую сессию;
                - total_energy_kwh (numeric) — суммарный объём отпущенной энергии в кВт·ч.

        Example:
            Возвращаемое значение:

            {
                "total_sessions": 1250,
                "total_revenue": 18540.75,
                "avg_revenue_per_station": 1545.06,
                "avg_revenue_per_session": 14.83,
                "total_energy_kwh": 38250.40
            }

        Notes:
            - Для предотвращения деления на ноль используется функция
            `NULLIF()`.
            - При отсутствии данных возвращаются значения `0`
            благодаря использованию `COALESCE()`.
            - Средняя выручка на станцию рассчитывается по количеству
            уникальных `station_id`.
        """
        q = """
            SELECT 
                COUNT(*) AS total_sessions
            ,    
                COALESCE(
                    SUM(cs.gross_revenue)
                    FILTER (WHERE cs.state = 'COMPLETED'),
                0) AS total_revenue
            ,
                COALESCE(
                    SUM(cs.gross_revenue) FILTER(WHERE cs.state = 'COMPLETED')
                    /
                    NULLIF(COUNT(DISTINCT cs.station_id), 0),
                    0
                ) AS avg_revenue_per_station
            ,
                COALESCE(
                    SUM(cs.gross_revenue) FILTER(WHERE cs.state = 'COMPLETED')
                    /
                    NULLIF(COUNT(*) FILTER (WHERE cs.state = 'COMPLETED'), 0),
                    0
                ) AS avg_revenue_per_session
            ,
                COALESCE(
                    SUM(cs.energy_kwh)
                    FILTER(WHERE cs.state = 'COMPLETED'),
                    0
                    ) AS total_energy_kwh
            
            FROM charging_sessions_fact cs

            WHERE user_id = $1
                AND cs.start_ts >= $2
                AND cs.start_ts < $3
            """
        async with self.db.pool.acquire() as conn:
            return await conn.fetchrow(q, user_id, date_from, date_to)

    
    async def get_utilisation_metrics(
        self, 
        user_id:int, 
        date_from: datetime=None, 
        date_to:datetime=None
    ) -> Record | None:
        """
        Получает данные, необходимые для расчёта утилизации зарядной инфраструктуры
        за указанный период.
        Выполняет агрегацию по таблице `charging_sessions_fact` и возвращает:
        - суммарное время зарядки завершённых сессий (`charging_minutes`);
        - количество уникальных зарядных точек (`evse_count`), участвовавших
        в сессиях за выбранный период.
        В расчёт времени зарядки включаются только сессии со статусом
        `COMPLETED`.
        Args:
            user_id (int): Идентификатор пользователя.
            date_from (datetime, optional): Начало периода выборки (включительно).
            date_to (datetime, optional): Конец периода выборки (не включительно).
        Returns:
            asyncpg.Record:
                Запись с агрегированными значениями:

                - charging_minutes (float) — суммарная продолжительность
                завершённых зарядных сессий в минутах;
                - evse_count (int) — количество уникальных EVSE.
        Example:
            Возвращаемое значение:
            {
                "charging_minutes": 1250,
                "evse_count": 8
            }
        """
        q = """
            SELECT 
                COALESCE(
                    SUM(cs.charge_duration_minutes)
                        FILTER (WHERE cs.state = 'COMPLETED')
                    , 0
                )
                AS charging_minutes
                ,
                COUNT(DISTINCT cs.evse_path) AS evse_count
            FROM charging_sessions_fact cs
            WHERE user_id = $1
                AND cs.start_ts >= $2
                AND cs.start_ts < $3
            """
        async with self.db.pool.acquire() as conn:
            return await conn.fetchrow(q, user_id, date_from, date_to)
        

    async def get_margin_metrics(
        self, 
        user_id, 
        date_from: datetime, 
        date_to:datetime
    ) -> Record:
        """
        Получает агрегированные финансовые показатели за указанный период.

        Выполняет расчёт общей выручки, дохода партнёра и валовой маржи
        по завершённым зарядным сессиям (`COMPLETED`).

        Args:
            user_id (int): Идентификатор пользователя.
            date_from (datetime): Начало периода выборки (включительно).
            date_to (datetime): Конец периода выборки (не включительно).

        Returns:
            asyncpg.Record | None:
                Запись с финансовыми показателями:

                - total_revenue (numeric) — общая выручка;
                - partner_revenue (numeric) — доход партнёра;
                - gross_margin (numeric) — валовая маржа оператора
                (разница между общей выручкой и доходом партнёра).

                Может вернуть `None`, если запрос не выполнился или
                данные отсутствуют.

        Example:
            {
                "total_revenue": 10000.00,
                "partner_revenue": 7500.00,
                "gross_margin": 2500.00
            }

        Notes:
            - В расчёт включаются только сессии со статусом `COMPLETED`.
            - При отсутствии данных значения агрегатов заменяются на `0`
            с помощью функции `COALESCE()`.
            - Валовая маржа рассчитывается как:

                gross_margin = total_revenue - partner_revenue
        """
        q = """
            SELECT
                COALESCE(
                    SUM(cs.gross_revenue) 
                        FILTER (WHERE cs.state = 'COMPLETED')
                        , 0
                ) AS total_revenue
                ,
                COALESCE(
                    SUM(cs.partner_revenue) 
                        FILTER (WHERE cs.state = 'COMPLETED')
                        , 0
                ) AS partner_revenue
                ,
                COALESCE(
                    SUM(cs.gross_revenue) 
                        FILTER(WHERE cs.state = 'COMPLETED')
                    -
                    SUM(cs.partner_revenue)
                        FILTER(WHERE cs.state = 'COMPLETED')
                        , 0
                ) AS gross_margin
            FROM charging_sessions_fact cs
            WHERE user_id = $1
                AND cs.start_ts >= $2
                AND cs.start_ts < $3
            """
        async with self.db.pool.acquire() as conn:
            return await conn.fetchrow(q, user_id, date_from, date_to)


    async def get_connected_station(self, user_id: int) -> Record:
        """
        Получает информацию о количестве зарядных станций пользователя
        и их текущем статусе подключения.

        Метод выполняет агрегацию данных по таблице `info_station`
        и возвращает:

        - общее количество уникальных станций;
        - количество станций, находящихся в статусе подключения (`connected = true`).

        Args:
            user_id (int): Идентификатор пользователя.

        Returns:
            asyncpg.Record:
                Запись со статистикой по станциям:

                - total_station (int) — общее количество уникальных зарядных станций;
                - connected_stations (int) — количество подключённых станций.

        Example:
            Возвращаемое значение:

            {
                "total_station": 25,
                "connected_stations": 22
            }

        Notes:
            - Общее количество станций определяется по уникальным
            значениям `station_id`.
            - Подключёнными считаются станции, у которых поле
            `connected` имеет значение `true`.
        """
        q = f"""
            SELECT 
                COUNT(DISTINCT  s.station_id) AS total_station,
                COUNT(*) FILTER (
                    WHERE s.connected = true
                ) AS connected_stations
            FROM info_station s
                WHERE s.user_id = $1
            """
        async with self.db.pool.acquire() as conn:
            return await conn.fetchrow(q, user_id)
        

    async def get_station_revenue_stats(
        self, 
        user_id:int, 
        date_from:datetime, 
        date_to:datetime
    ) -> list[Record]:
        q = """
            SELECT 
                cs.station_id
                ,
                MAX(s.location_name) AS station_name
                ,
                COALESCE(
                    SUM(cs.gross_revenue) 
                        FILTER (WHERE cs.state = 'COMPLETED')
                        , 
                        0
                ) AS total_revenue
                ,
                COALESCE(
                    SUM(cs.charge_duration_minutes)
                        FILTER (WHERE cs.state = 'COMPLETED')
                    , 
                    0
                ) AS charging_minutes
                ,
                COUNT(DISTINCT cs.evse_path) AS evse_count

            FROM charging_sessions_fact cs

            LEFT JOIN info_station s
                ON s.id = cs.station_id
                    AND s.user_id = cs.user_id

            WHERE cs.user_id = $1
                AND cs.start_ts >= $2
                AND cs.end_ts < $3

            GROUP BY cs.station_id
            """
        async with self.db.pool.acquire() as conn:
            return await conn.fetch(q, user_id, date_from, date_to)