from backend.api.routers.auth.connect_operator.db import ConnectOperatorDB
from backend.api.routers.auth.users import Users
from core.base_db import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.base_db import Base






class Manager:
    def __init__(self, base_db: "Base"):
        self.base_db = base_db
        self.users = Users(base_db)
        self.connect_operator = ConnectOperatorDB(base_db)

    