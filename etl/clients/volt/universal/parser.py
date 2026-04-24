
import pandas as pd

class Parser:
    

    @staticmethod
    def to_df(data:list[dict], type_method: str):
        res = []
        if type_method == 'chargepoints':
            for d in data:
                location = d['location']
                base = {
                    "station_id": d['id'],
                    "key": d['key'],
                    "name": d['name'],
                    "serialNumber": d['serialNumber'],
                    "state": d["state"],
                    "connected": d['connected'],
                    "lastSeen": d["lastSeen"],
                    "model": d['model'],
                    "vendor": d['vendor'],
                    "protocol": d['protocol'],
                    "operatorId": d['operatorId'],
                    "operatorName": d['operatorName'],
                    "location_id": location['id'],
                    "location_name": location['name'], 
                    "location_address": location['address'], 
                    "location_city": location['city'], 
                    "location_latitude": location['latitude'], 
                    "location_longitude": location['longitude']
                }

                res.append(base)
            return pd.DataFrame(res)
        return pd.DataFrame(data)