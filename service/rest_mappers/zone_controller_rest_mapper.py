
from service.rest_mappers.base_rest_mapper import BaseRestMapper
from service.zone.zone_data_manager import ZoneDataManager
from service.zone.zone_controller import ZoneController
from datetime import datetime, timedelta
from service.zone.zone_timing_bo import ZoneTiming
from service.core import shared
from service.database.decision_dbo import DecisionDBO
from service.database.db_schema import DecisionHistory, EnumDecisionCodes, EnumReasonCodes
from service.system.settings_manager import SettingsManager

class ZoneControllerRestMapper(BaseRestMapper):

    FIELD_ID = 'id'
    FIELD_DURATION = 'duration'

    ERROR_TYPE_ZONE_NOT_FOUND = "Invalid ID - Zone not found"
    ERROR_TYPE_ZONE_ALREADY_ACTIVE = "Zone already active"
    ERROR_TYPE_UNABLE_TO_ACTIVATE_ZONE = "Unable to activate zone - Check error logs for more details"
    ERROR_TYPE_UNABLE_TO_DEACTIVATE_ZONE = "Unable to deactivate zone - Check error logs for more details"

    ERROR_TYPE_ZONE_NOT_ACTIVE = "Zone not active"
    ERROR_TYPE_NO_PIN_CONFIGURED_FOR_ZONE = "RPI Pin and relay not configured for this zone. Please set one before trying to activate."
    ERROR_TYPE_KILL_SWITCH_IS_ACTIVE = "Kill switch is active. Unable to activate zone."
    def __init__(self):
        self.zdm = ZoneDataManager()
        self.zc = ZoneController()
        self.decisionDbo = DecisionDBO()
        self.settingsMgr = SettingsManager()

    def activateZone(self, json_data):
        
        shared.logger.debug(self, "activateZone entered")
        zone_id = self.getKeyOrThrowException(json_data, self.FIELD_ID, json_data)
        duration = self.getKeyOrThrowException(json_data, self.FIELD_DURATION, json_data)
        
        self.validateIsProvidedAndInt(zone_id, ZoneControllerRestMapper.FIELD_ID)
        self.validateIsProvidedAndInt(duration, ZoneControllerRestMapper.FIELD_DURATION)

        # Fetch zone using ID
        zone = self.zdm.retrieveZone(zone_id)

        if zone is not None:

            if zone.id in ZoneController.activeZones:
                self.raiseBadRequestException(self.FIELD_ID, self.ERROR_TYPE_ZONE_ALREADY_ACTIVE)
            
            # check if the kill switch is on
            if self.settingsMgr.getKillSwitch() is True:
                self.raiseBadRequestException(self.FIELD_ID, self.ERROR_TYPE_KILL_SWITCH_IS_ACTIVE)
            
            shared.logger.debug(self, "Checking if pin config is set")
            if zone.pin_config is None:
                shared.logger.debug(self, "Pin Config not set. Throwing error.")
                self.raiseServerErrorException(self.ERROR_TYPE_NO_PIN_CONFIGURED_FOR_ZONE)

            # Set to current time plus the requested run time
            start_time = datetime.now()
            end_time = start_time + timedelta(minutes=int(duration))

            # create a zone timing object
            zto = ZoneTiming.initialize(zone, start_time, end_time)

            shared.logger.debug(self, "Manual Activation Requested for zone: " + zone.name + ". End time = " + str(end_time))
            
            # Activating zone
            if self.zc.activateZone(zto, reasonCode=EnumReasonCodes.Manual) is False:
                self.raiseServerErrorException(self.ERROR_TYPE_UNABLE_TO_ACTIVATE_ZONE)
            

            return self.returnSuccessfulResponse()
        else:
            self.raiseBadRequestException(self.FIELD_ID, self.ERROR_TYPE_ZONE_NOT_FOUND,json_data)

        

    def deactivateZone(self, json_data):
        zone_id = json_data[ZoneControllerRestMapper.FIELD_ID]
        self.validateIsProvidedAndInt(zone_id, ZoneControllerRestMapper.FIELD_ID)
        
        
        zone = self.zdm.retrieveZone(zone_id)

        if zone is not None:
            # Check if the zone is active, otherwise throw an error
            if zone.id not in ZoneController.activeZones:
                self.raiseBadRequestException(self.FIELD_ID, self.ERROR_TYPE_ZONE_NOT_ACTIVE)

            
            # Deactivate the zone
            if not self.zc.deactivateZone(zone, decisionHistoryReasonCode=EnumReasonCodes.Manual, overrideEndTime=datetime.now()):
                self.raiseServerErrorException(self.ERROR_TYPE_UNABLE_TO_DEACTIVATE_ZONE)

        return self.returnSuccessfulResponse()
    
    