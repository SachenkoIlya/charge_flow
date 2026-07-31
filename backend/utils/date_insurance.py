# from backend.core.schemas import DashboardFilterSchema
from datetime import datetime, timezone, timedelta


def date_insurance(
    date_from: datetime=None, 
    date_to:datetime=None
) -> tuple[datetime, datetime]:
    today = datetime.now()
    if date_from is None:
        date_from = today.strftime('%d.%m.%Y')

    if date_to is None:
        date_to = date_from

    date_from = datetime.strptime(date_from, "%d.%m.%Y")
    date_to = datetime.strptime(date_to, "%d.%m.%Y") + timedelta(days=1)

    date_from = date_from.replace(tzinfo=timezone.utc)
    date_to = date_to.replace(tzinfo=timezone.utc)
    return date_from, date_to



def date_insurance_from_dict(data: dict) -> tuple[datetime, datetime]:
    today = datetime.now()
    date_from = None
    date_to = None
    
    if not data.get('date_from'):
        date_from = today.strftime('%d.%m.%Y')

    if not data.get('date_to'):
        date_to = date_from

    date_from = datetime.strptime(data.get('date_from'), "%d.%m.%Y")
    date_to = datetime.strptime(data.get('date_to'), "%d.%m.%Y") + timedelta(days=1)

    date_from = date_from.replace(tzinfo=timezone.utc)
    date_to = date_to.replace(tzinfo=timezone.utc)
    return date_from, date_to
