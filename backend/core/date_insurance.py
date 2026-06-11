from backend.core.schemas import DashboardFilterSchema
from datetime import datetime, timezone, timedelta


def date_insurance(data: DashboardFilterSchema) -> tuple[datetime, datetime]:
    today = datetime.now()
    if not data.date_from:
        data.date_from = today.strftime('%d.%m.%Y')

    if not data.date_to:
        data.date_to = data.date_from

    date_from = datetime.strptime(data.date_from, "%d.%m.%Y")
    date_to = datetime.strptime(data.date_to, "%d.%m.%Y") + timedelta(days=1)

    date_from = date_from.replace(tzinfo=timezone.utc)
    date_to = date_to.replace(tzinfo=timezone.utc)
    return date_from, date_to
