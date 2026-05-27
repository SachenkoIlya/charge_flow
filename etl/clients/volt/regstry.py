
from .universal.client import BaseVoltApi



class Endpoints:
    
    base_url = 'https://api.volt-ev.ru/quantum/rest'
    endpoints = {
        'chargepoints': 'partner/v1/chargepoints',
        'charging_sessions': 'partner/v1/charging-sessions'
    }


    @classmethod
    def get_full_url(cls, type_method: str):
        endpoint = cls.endpoints.get(type_method)
        
        if endpoint is None:
            raise ValueError(f"Unknown endpoint: {type_method}")

        return f"{cls.base_url}/{endpoint}"
        

class RegstryVolt:

    registry = {
        'chargepoints' : BaseVoltApi(
            type_method='chargepoints',
            method='get',
            url=Endpoints.get_full_url('chargepoints'),
            body={
                "limit": 50, 
                "offset": 0
            },
        ),
        'charging_sessions': BaseVoltApi(
            type_method='charging_sessions',
            method='get',
            url=Endpoints.get_full_url('charging_sessions'),
            body={
                "limit": 50, 
                "offset": 0,
            },
        )
    }
    
    