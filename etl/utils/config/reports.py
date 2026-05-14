

from ..policy.policy import ReportPolicy
from datetime import timedelta, datetime

from core.security.settings import settings
from core.logger.logger import logger

class ReportConfig:
  
    TYPE_METHODS = {
        'volt': ['chargepoints', 'charging_sessions'],
        'sictronics': ['default']
    }


    REPORT_POLICIES = {
        'volt': {
            'chargepoints': ReportPolicy(
                name="chargepoints",
                paid_interval=timedelta(
                    days=settings.CHARGEPOINTS_INTERVAL
                ),
                first_run_days_back=0,
            ),
       
            'charging_sessions': ReportPolicy(
                name="charging_sessions",
                paid_interval=timedelta(
                    hours=settings.CHARGING_SESSIONS_INTERVAL   
                ),
                first_run_days_back=30,
            ),
        },
        'sictronics': {},
      
    }



    @staticmethod
    def should_run(policy:"ReportPolicy", last_success_from_db: datetime|None, now: datetime):
        logger.debug(f"policy: {policy}".upper())
        logger.debug(f"last_success_from_db: {last_success_from_db}".upper())
        logger.debug(f"now: {now}".upper())
        
        if last_success_from_db is None:
            return now - timedelta(days=policy.first_run_days_back)
        # если прошло достаточно времени
        if now - last_success_from_db >= policy.paid_interval:
            return last_success_from_db

        return None