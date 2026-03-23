from backend.database.base import Base

from backend.main.db import RunRepository
from backend.core.db import RunPiplines
from backend.runtime.export.db import RunExport

class Manager:
    def __init__(self, base_db: "Base"):
        self.base_db = base_db

        self.run_reposityry = RunRepository(base_db)
        self.run_piplines = RunPiplines(base_db)
        self.run_export = RunExport(base_db)