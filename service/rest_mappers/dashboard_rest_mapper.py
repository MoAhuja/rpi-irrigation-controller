from service.rest_mappers.base_rest_mapper import BaseRestMapper
from service.system.settings_manager import SettingsManager
from service.zone.zone_controller import ZoneController
from service.zone.zone_data_manager import ZoneDataManager
from service.database.decision_dbo import DecisionDBO
from service.utilities.conversion import Conversions
from service.core.scheduler import Scheduler


class DashboardRestMapper(BaseRestMapper):

    FIELD_SYSTEM = "system_settings"
    FIELD_RAIN_DELAY = "rain_delay"
    FIELD_KILL_SWITCH = "kill_switch"
    FIELD_LOCATION = "location"
    FIELD_CITY = "city"
    FIELD_COUNTRY = "country"

    # Zone fields
    FIELD_ID = "id"
    FIELD_ZONES = "zones"
    FIELD_NAME = "name"
    FIELD_DESCRIPTION = "description"
    FIELD_ENABLED = "enabled"
    FIELD_LAST_RUN = "last_run"
    FIELD_START = "start"
    FIELD_END = "end"
    FIELD_NEXT_RUN = "next_run"
    FIELD_IS_RUNNING = "is_running"

    def __init__(self):
        self.settingsManager = SettingsManager()
        self.zc = ZoneController()
        self.zdm = ZoneDataManager()
        self.decisionDBO = DecisionDBO()
        self.scheduler = Scheduler()



    
    def getDashboard(self):

        result = {}

        # Get the Rain Delay value
        systemDict = {}

        # System Dashboard
            # Rain Delay Status
        systemDict[DashboardRestMapper.FIELD_RAIN_DELAY] = self.settingsManager.getRainDelay()
        # Kill Switch Status
        systemDict[DashboardRestMapper.FIELD_KILL_SWITCH] = self.settingsManager.getKillSwitch()
        # Current Location
        systemDict[DashboardRestMapper.FIELD_CITY] = self.settingsManager.getCity()
        systemDict[DashboardRestMapper.FIELD_COUNTRY] = self.settingsManager.getCountry()

        # Attach to overall result
        result[DashboardRestMapper.FIELD_SYSTEM] = systemDict
        # Predicted Forecast (Future)

        zone_array = []
        # Zone Dashboard
        # Fetch all the zones
        zones = self.zdm.retrieveAllZones()
        for zone in zones:
            zoneDict = {}
            zoneDict[DashboardRestMapper.FIELD_ID] = zone.id
            zoneDict[DashboardRestMapper.FIELD_NAME] = zone.name
            zoneDict[DashboardRestMapper.FIELD_DESCRIPTION] = zone.description
            zoneDict[DashboardRestMapper.FIELD_ENABLED] = zone.enabled
            zoneDict[DashboardRestMapper.FIELD_IS_RUNNING] = zone.id in ZoneController.activeZones

            # Query activation history table
            lastRunDecisionHistoryRecord = self.decisionDBO.fetchLastRunRecord(zone.id)
            lastRunDict = {}
            if lastRunDecisionHistoryRecord is not None:
                lastRunDict[DashboardRestMapper.FIELD_START] = Conversions.convertRainDelayDateTimeToString(lastRunDecisionHistoryRecord.start_time)
                lastRunDict[DashboardRestMapper.FIELD_END] = Conversions.convertRainDelayDateTimeToString(lastRunDecisionHistoryRecord.end_time)
                zoneDict[DashboardRestMapper.FIELD_LAST_RUN] = lastRunDict
            
            # Query the schedule table for the next run
            start_time, end_time = self.scheduler.getNextRunStartAndEndForZone(zone.id)
            nextRunDict = {}
            if start_time is not None and end_time is not None:
                nextRunDict[DashboardRestMapper.FIELD_START] = Conversions.convertRainDelayDateTimeToString(start_time)
                nextRunDict[DashboardRestMapper.FIELD_END] = Conversions.convertRainDelayDateTimeToString(end_time)
                zoneDict[DashboardRestMapper.FIELD_NEXT_RUN] = nextRunDict
            
            
            zone_array.append(zoneDict)

        
        result[DashboardRestMapper.FIELD_ZONES] = zone_array
        
        return self.returnSuccessfulResponse(result)