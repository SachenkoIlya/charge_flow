

from ..policy.policy import ReportPolicy
from datetime import timedelta, datetime
from dotenv import load_dotenv
import os
load_dotenv()

class ReportConfig:
    # "chargepoints" charging_sessions
    # chargepoints
    TYPE_METHODS = {
        'volt': ['chargepoints', 'charging_sessions'],
        'sictronics': ['default']
    }


    REPORT_POLICIES = {
        'volt': {
            'chargepoints': ReportPolicy(
                name="chargepoints",
                paid_interval=timedelta(
                    days=int(os.getenv('CHARGEPOINTS_INTERVAL', '3'))
                ),
                first_run_days_back=0,
            ),
       
            'charging_sessions': ReportPolicy(
                name="charging_sessions",
                paid_interval=timedelta(
                    hours=int(os.getenv('CHARGING_SESSIONS_INTERVAL', '6'))
                ),
                first_run_days_back=30,
            ),
        },
        'sictronics': {},
      
    }



    @staticmethod
    def should_run(policy:"ReportPolicy", last_success_from_db: datetime|None, now: datetime):
        if last_success_from_db is None:
            return now - timedelta(days=policy.first_run_days_back)
        # если прошло достаточно времени
        if now - last_success_from_db >= policy.paid_interval:
            return last_success_from_db

        return None