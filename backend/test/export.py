

from backend.database.base import Base
from backend.utils.context.ctx import Ctx
from backend.utils.context.run_ctx import RunContext
from backend.users.users import Users
from datetime import datetime, timezone
from backend.runtime.export.export import ExportFromBi
import asyncio

async def test_export(run_mode: str, run_id:str, type_method: str, operator: str, base_db:"Base"):
    ctx = Ctx(
        run_mode = run_mode,
        type_method = type_method,
        run_id = run_id,
        operator = operator,
        base_db = base_db,
    )

    rows = await ctx.db.run_reposityry.get_users()

    
    users = [Users.from_db(row) for row in rows]
    
    run_contexts = [
        RunContext(
            now=datetime.now(timezone.utc),
            user=user,
            last_success=datetime.now(timezone.utc),
            
        )
        for user in users
    ]

    await ExportFromBi.run_export_task(
        ctx=ctx,
        run_contexts=run_contexts
    )



    

async def main(run_mode: str, operator:str):
    base_db = Base()
    type_method = 'charging_sessions'
    run_id = '4c845dfdfa104af696604065dcd83408'
    await base_db.connect()
    try:
        await test_export(
            run_mode=run_mode,
            run_id=run_id,
            type_method=type_method,
            operator=operator,
            base_db=base_db
        )
    finally:
        await base_db.close()


if __name__ == '__main__':
    import sys

    operator = sys.argv[1]
    run_mode = sys.argv[2]
    
    
    asyncio.run(main(run_mode=run_mode, operator=operator))
    # py -m backend.test.export volt test