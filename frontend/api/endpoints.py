
class Endpoints:
    """Реестр эндпоинтов для маппинга внутренних имен на URL и HTTP-методы.

    Хранит конфигурацию доступных маршрутов бэкенд-API и предоставляет
    интерфейс для безопасного получения метаданных запроса по строгому ключу.

    Attributes:
        endpoints (dict): Словарь, где ключ — внутреннее имя действия,
            а значение — словарь с параметрами 'url' (относительный путь)
            и 'method' (HTTP-метод в нижнем регистре).
    """
    endpoints = {
        'dashboard_stats' :{
            'url': 'dashboard/stats',
            'method': 'post'
        },
        'operators_connect' :{
            'url': 'operators/connect',
            'method': 'post'
        },
        'auth_register' :{
            'url': 'auth/register',
            'method': 'post'
        },
        'company' :{
            'url': 'dashboard/companies',
            'method': 'get'
        },
        'auth_login' :{
            'url': 'auth/login',
            'method': 'post'
        },
        'stations': {
            'url': 'v1/stations/stations',
            'method': 'get'
        },
        'investments': {
            'url': 'finance/investments-and-expenses',
            'method': 'post'
        },
        'system': {
            'url': 'v1/system/monitoring',
            'method': 'post'
        },
        'summary': {
            'url':'v1/dashboard/summary',
            'method': 'post'
        },
        'finance': {
            'url':'v1/dashboard/finance',
            'method': 'post'
        }
    }
    
    
    @classmethod
    def get_data_endpoints(cls, endpoint_name) -> tuple[str, str]:
        """Возвращает URL и HTTP-метод для указанного имени эндпоинта."""
        data = cls.endpoints.get(endpoint_name)
        if not data:
            raise ValueError(f'Endpoint {endpoint_name} not found')
        return data['url'], data['method'] 
