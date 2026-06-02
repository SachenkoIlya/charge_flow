
class Endpoints:
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
            'url': 'stations/stations',
            'method': 'post'
        }
    }
    
    @classmethod
    def get_data_endpoints(cls, endpoint_name):
        data = cls.endpoints.get(endpoint_name)
        if not data:
            raise ValueError(f'Endpoint {endpoint_name} not found')
        return data['url'], data['method'] 
