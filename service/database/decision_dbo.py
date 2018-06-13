
# from datetime import datetime
# from service.utilities.conversion import Conversions
from service.database.base_db_operations import BaseDBOperations
from service.utilities.logger import Logger
 
from service.database.db_schema import Zone, DecisionHistory, EnumDecisionCodes, EnumReasonCodes

class DecisionDBO(BaseDBOperations):

    def insertDecisionWithAllInfo(zone_id, decision, reason, schedule_start, schedule_end, current_temp, current_3hour_forecast, current_daily_forecast, temperature_enabled, temperature_lower_limit, temperature_upper_limit, rain_enabled, rain_short_term_limit, rain_daily_limit)

        self.initialize()
        DecisionHistory dh = DecisionHistory(zone_id=zone_id, current_temperature = current_temp, current_3hour_forecast = current_3hour_forecast, current_daily_forecast = current_daily_forecast, temperature_enabled = temperature_enabled, temperature_lower_limit = temperature_lower_limit, rain_enabled = rain_enabled,rain_short_term_limit = rain_short_term_limit, rain_daily_limit = rain_daily_limit, start_time=schedule_start, end_time = schedule_end, decision=decision, reason=reason)
        self.add(dh)
        self.flush()
    

