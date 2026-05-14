from core.logger.logger import logger
from core.security.settings import settings

CHARGIN_SESSION = 'charging_sessions'
CHARGEPOINTS = 'chargepoints'

TABLE_NAME_MAP = {
        'dev': {
            'charging_sessions': 'charging_sessions_fact_test',
            'chargepoints': 'info_station_test',
        },
        'test':  {
            'charging_sessions': 'charging_sessions_fact_test',
            'chargepoints': 'info_station_test',
        },
        'prod':  {
            'charging_sessions': 'charging_sessions_fact',
            'chargepoints': 'info_station',
        },
    }

def get_table_name_map(type_method: str) -> str:
    """Возвращает имя таблицы бд в зависимости от mode 
        prod, dev, test подятгивается из.env (MODE)
        имена таблиц для mode dev и test имеют префиксы _test
        Например:
            prod = charging_sessions_fact
            dev = charging_sessions_fact_test
            test = charging_sessions_fact_test
    """
    table_name = TABLE_NAME_MAP.get(settings.MODE).get(type_method)
    logger.debug(f"MODE: {settings.MODE}, возвращаю имя таблицы: {table_name}".upper())
    return table_name 
    
