from etl.clients.volt.universal.parser import ChargePointParser, ChargeSessionsParser
class BrokenParser:
    pass

PARSER = {
        'broken': {
            'charging_sessions': BrokenParser,
        },
        'volt': {
            'chargepoints': ChargePointParser,
            'charging_sessions': ChargeSessionsParser,
        },
        'sitronics': {
            'default': 'default'
        }
    }
def get_parser(operator: str, type_method: str):
    parser = PARSER.get(operator, {}).get(type_method)

    if not parser:
        raise ValueError(
            f"Parser not found for operator='{operator}', "
            f"type_method='{type_method}'"
        )

    return parser