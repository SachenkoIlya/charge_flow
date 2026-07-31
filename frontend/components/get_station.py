from fastapi import Request

from frontend.api.client import frontend_api

def prepare_station(selected_station: list[dict]) -> dict:
    return  {
        str(station_id): f"{s['label']} · {station_key}"
        for s in selected_station
        for station_id, station_key 
        in zip(
            s['station_ids'],
            s['station_keys']
        )
    }

async def _get_selected_station(
    request: Request, 
    endpoint_name:str='stations'
) -> dict:
    
    selected_station = await frontend_api(
        endpoint_name=endpoint_name,
        request=request,
    )
    return prepare_station(selected_station)

