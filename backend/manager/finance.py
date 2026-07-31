from backend.api.routers.investments.investments_and_expenses.services.services import InvestmentsAndExpensesRepository
from backend.api.routers.user.stations.service.metrics import StationInfo
from core.base_db import Base


class ManagerFinance:
    def __init__(self, base_db: "Base"):
        self._investments_and_expenses = InvestmentsAndExpensesRepository(base_db)
        self._station_info = StationInfo(base_db)
    @property
    def investments(self):
        return self._investments_and_expenses
    @property
    def station_info(self):
        return self._station_info
    