from service.zone.zone_rpi_controller import ZoneRPIController
from service.core import shared, shared_events
from service.zone.zone_data_manager import ZoneDataManager
from service.zone.zone_timing_bo import ZoneTiming
from service.system.settings_manager import SettingsManager
from service.database.db_schema import EnumReasonCodes
from datetime import datetime

import json
class ZoneController():

    activeZones = {}

    def __init__(self):
        shared_events.event_publisher.register(self, False, True, False, False, listenForKillSwitchUpdates=True)

        self.zrpi_controller = ZoneRPIController()
        self.zdm = ZoneDataManager()
        self.settingsManager = SettingsManager()
    
        
    # TODO: Add event to listen for kill switch
        # TODO:Write an entry to the decision history table to indicate all zones were shutoff due to kil switch (reason code: KillSwitch?)
    
    def eventKillSwitchUpdated(self):
        killSwitch = self.settingsManager.getKillSwitch()

        if killSwitch is True:
            self.deactivateAllZones(decisionHistoryReasonCode=EnumReasonCodes.KillSwitch)

    def eventRainDelayUpdated(self, rainDelayDate):

        shared.logger.debug(self, "Received event: Rain delay updated")
        
        # Check if hte rain delay value is is the future. If so, stop all active zones.
        if datetime.now() < rainDelayDate:
            self.deactivateAllZones()

    def activateZone(self, zonetimingObj):

        result = False
        shared.logger.debug(self, "ActivateZone - Waiting to acquire lock: lockActiveZones")
        shared.lockActiveZones.acquire()
        try:

            # If the zone is already active, skip this directive.
            if zonetimingObj.zone.id in ZoneController.activeZones:
                shared.logger.info(self, "Zone is already active")
                return True


            shared.logger.debug(self,"Activating Zone")
            
            if self.zrpi_controller.activateZone(zonetimingObj.zone):
                shared.logger.debug(self,"Adding zone '" + zonetimingObj.zone.name + "' to list of active zones")
                ZoneController.activeZones[zonetimingObj.zone.id] = zonetimingObj
                result = True

        finally:
            shared.lockActiveZones.release()
            shared.logger.debug(self, "ActivateZone - releasing lock: lockActiveZones")
        
        shared.logger.debug(self, "Activating Zone Result = " + str(result))
        return result

    def deactivateZones(self, listOfKeysToDeactivate):
        
        shared.logger.debug(self, "deactivateZones - Waiting to acquire lock: lockActiveZones")
        shared.lockActiveZones.acquire()
        

        try:
            for x in listOfKeysToDeactivate:
                # Fetch the zonetiming object and deactivate teh zone
                self.zrpi_controller.deactivateZone(activateZone[x].zone)

                # Remove the zone from the list of active zones
                del ZoneController.activeZones[x]

        finally:
            shared.lockActiveZones.release()
            shared.logger.debug(self, "deactivateZones - releasing lock: lockActiveZones")

    def deactivateZone(self, zone):
        result = False
        shared.logger.debug(self, "deactivateZone - Waiting to acquire lock: lockActiveZones")
        shared.lockActiveZones.acquire()
        
        try:
            # Call the RPI controller to deactivate the zone
            if self.zrpi_controller.deactivateZone(zone):

                # Remove the zone from the list of active zones
                del ZoneController.activeZones[zone.id]

                result = True
                
        finally:
            shared.lockActiveZones.release()
            shared.logger.debug(self, "deactivateZones- releasing lock: lockActiveZones")
        
        return result


    def deactivateAllZones(self, decisionHistoryReasonCode=None):
    
        result = False
        shared.logger.debug(self,"Deactivating All Zones")
        shared.logger.debug(self, "deactivateAllZones - Waiting to acquire lock: lockActiveZones")
        shared.lockActiveZones.acquire()
        
        try:
            for key, activeZone in ZoneController.activeZones.items():
                shared.logger.debug(self, "Deactivating -> " + key + "-->" + activeZone.zone.name)

                # TODO: Add logic to look at the decision history reason code and insert decision history events for each class

                #Call the RPI controller to deactivate this zone
                self.zrpi_controller.deactivateZone(zone)
            
            # Reset back to an empty hashmap
            ZoneController.activeZones = {}
            result = True

        finally:
            shared.lockActiveZones.release()
            shared.logger.debug(self, "deactivateAllZones - releasing lock: lockActiveZones")

        return result

    # def manuallyDeactivateZone(self, zone):

    #     # Check if zone is in the list of active zones
    #     if self.activeZones[zone.id] is not None:
    #         # TODO: What if a manual deactiate is called while he zone list is being?? Will this crash it?
    #         del self.activeZones[zone.id]
    #         shared.logger.info(self,"Zone " + str(zone.id) + "has been MANUALLY deactivated")

    #         # TODO: insert a deactivation history event
    
    # def manuallyActivateZone(self, zone, end_time):
        # TODO: Check if the zone is already active
        # TODO: Inject this zone into list of active zonesp
     
        # return False