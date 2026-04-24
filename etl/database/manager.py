from etl.runtime.export.db import RunExport
from etl.main.db import RunRepository
from etl.core.db import RunPiplines
from core.base_db import Base

class Manager:
    def __init__(self, base_db: "Base"):
        self.base_db = base_db

        self.run_reposityry = RunRepository(base_db)
        self.run_piplines = RunPiplines(base_db)
        self.run_export = RunExport(base_db)