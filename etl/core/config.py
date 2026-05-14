from etl.clients.volt.regstry import RegstryVolt
from etl.runtime.export.export import ExportFromBi


class RegistryNotFoundError(Exception):
    pass
class ScenarioExportNotFoundError(Exception):
    pass


MAP_CLS = {
        'volt': RegstryVolt
    }
MAP_SCENARIO_EXPORT = {
    'bi': {
        'volt': {
            'charging_sessions': ExportFromBi.run_export_task,
            'chargepoints': ExportFromBi.run_export_task
        }
        
    }
}

def get_registry_report(operator:str):
    report = MAP_CLS.get(operator)
    if not report:
        raise RegistryNotFoundError(
            f'Operator "{operator}" not found'
        )
    return report
    

def get_export_task(operator:str, type_method:str, scenario:str='bi'):
    export_scenario = (
        MAP_SCENARIO_EXPORT
        .get(scenario)
        .get(operator)
        .get(type_method)
    )
    if not export_scenario:
        raise ScenarioExportNotFoundError(
            f'Export task not found:\n'
            f'scenario="{scenario}",\n'
            f'operator="{operator}",\n'
            f'type_method="{type_method}"'
        )
    return export_scenario