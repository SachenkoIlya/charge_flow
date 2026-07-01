
from core.base_db import Base
from backend.api.routers.auth.register.service.service import RegistrationService


class UserAuthManager:
    def __init__(self, db: "Base"):
        self.registration = RegistrationService(db)