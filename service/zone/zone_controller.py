from service.zone.zone_rpi_controller import ZoneRPIController
from service.core import shared, shared_events
from service.zone.zone_data_manager import ZoneDataManager
from service.zone.zone_timing_bo import ZoneTiming
from service.system.settings_manager import SettingsManager
from service.database.db_schema import EnumReasonCodes, EnumDecisionCodes, DecisionHistory
from service.database.decision_dbo import DecisionDBO
from datetime import datetime

import json
class ZoneController():

    activeZones = {}

    def __init__(self):
        shared_events.event_publisher.register(self, False, True, False, False, listenForKillSwitchUpdates=True)

        self.zrpi_controller = ZoneRPIController()
        self.zdm = ZoneDataManager()
        self.settingsManager = SettingsManager()
        self.decisionDBO = DecisionDBO()
    
        
    
    def eventKillSwitchUpdated(self):
        killSwitch = self.settingsManager.getKillSwitch()

        if killSwitch is True:
            self.deactivateAllZones(decisionHistoryReasonCode=EnumReasonCodes.KillSwitch, overrideEndTime=datetime.now())

    def eventRainDelayUpdated(self, rainDelayDate):

        shared.logger.debug(self, "Received event: Rain delay updated")
        
        # Check if hte rain delay value is is the future. If so, stop all active zones.
        if rainDelayDate is True and datetime.now() < rainDelayDate:
            self.deactivateAllZones()

    def activateZone(self, zonetimingObj, existingDecisionHistoryEvent=None, reasonCode=None):

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

                dh = DecisionHistory()

                if existingDecisionHistoryEvent is not None:
                    # Append to it
                    dh = existingDecisionHistoryEvent
                
                # Insert entry into decision history table
                self.insertDecisionHistoryEvent(dh, zonetimingObj, reasonCode, EnumDecisionCodes.ActivateZone)

                # publish the event indicating the watering has started
                shared_events.event_publisher.publishWateringStarted(zonetimingObj.zone.name)

                result = True

        finally:
            shared.lockActiveZones.release()
            shared.logger.debug(self, "ActivateZone - releasing lock: lockActiveZones")
        
        shared.logger.debug(self, "Activating Zone Result = " + str(result))
        return result

    def deactivateListOfZones(self, listOfKeysToDeactivate, decisionHistoryReasonCode=None):
 
        for x in listOfKeysToDeactivate:
            self.deactivateZone(ZoneController.activeZones[x].zone, decisionHistoryReasonCode)


    def deactivateZone(self, zone, decisionHistoryReasonCode=None, overrideEndTime=None):
        result = False
        shared.logger.debug(self, "deactivateZone - Waiting to acquire lock: lockActiveZones")
        shared.lockActiveZones.acquire()
        
        try:
            # Call the RPI controller to deactivate the zone
            if self.zrpi_controller.deactivateZone(zone):
                
                # Publish the event indicating the watering stopped
                shared_events.event_publisher.publishWateringStopped(zone.name)

                if decisionHistoryReasonCode is not None:
                    zoneTiming = ZoneController.activeZones[zone.id]

                    # Insert a decision event
                    dh = DecisionHistory()
                    self.insertDecisionHistoryEvent(decisionObject=dh, zoneTiming=zoneTiming, reasonCode=decisionHistoryReasonCode, decisionCode=EnumDecisionCodes.DeactivateZone,overrideEndTime=overrideEndTime)


                # Remove the zone from the list of active zones
                del ZoneController.activeZones[zone.id]

                result = True
                
        finally:
            shared.lockActiveZones.release()
            shared.logger.debug(self, "deactivateZones- releasing lock: lockActiveZones")
        
        return result

    def insertDecisionHistoryEvent(self, decisionObject, zoneTiming, reasonCode, decisionCode, overrideEndTime=None):
        shared.logger.debug(self,"insertDecisionHistoryEvent called. Data ==")
        
        decisionObject.zone_id = zoneTiming.zone.id
        decisionObject.start_time = zoneTiming.start_time

        # Allows for the end time to be overriden in the scenario where the zone is stopped manually
        if overrideEndTime is not None:
            decisionObject.end_time = overrideEndTime
        else:
            decisionObject.end_time = zoneTiming.end_time

        decisionObject.decision = decisionCode
        decisionObject.reason = reasonCode

        shared.logger.debug(self,str(decisionObject.zone_id))
        # shared.logger.debug(self,decisionObject.start_time)
        # shared.logger.debug(self,decisionObject.end_time)
        # shared.logger.debug(self,decisionObject.reasonCode)
        # shared.logger.debug(self,decisionObject.decisionCode)
        self.decisionDBO.insertDecisionEvent(decisionObject)

    def deactivateAllZones(self, decisionHistoryReasonCode=None, overrideEndTime=None):
    
        result = False
        shared.logger.debug(self,"Deactivating All Zones")
        shared.logger.debug(self, "deactivateAllZones - Waiting to acquire lock: lockActiveZones")
        shared.lockActiveZones.acquire()
        
        try:
            for key, activeZone in ZoneController.activeZones.items():
                shared.logger.debug(self, "Deactivating -> " + str(key) + "-->" + activeZone.zone.name)

                #Call the RPI controller to deactivate this zone
                if self.zrpi_controller.deactivateZone(activeZone.zone):
                    if decisionHistoryReasonCode is not None:
                        zoneTiming = ZoneController.activeZones[activeZone.zone.id]

                        # Insert a decision event
                        dh = DecisionHistory()
                        self.insertDecisionHistoryEvent(decisionObject=dh, zoneTiming=zoneTiming, reasonCode=decisionHistoryReasonCode, decisionCode=EnumDecisionCodes.DeactivateZone, overrideEndTime=overrideEndTime)

            
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