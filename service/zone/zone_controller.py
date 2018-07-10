from service.zone.zone_rpi_controller import ZoneRPIController
from service.core import shared
from service.zone.zone_data_manager import ZoneDataManager
from service.zone.zone_timing_bo import ZoneTiming

import json
class ZoneController():

    activeZones = {}

    def __init__(self):
        self.zrpi_controller = ZoneRPIController()
        self.zdm = ZoneDataManager()
    

    def activateZone(self, zonetimingObj):

        result = False
        shared.logger.debug(self, "ActivateZone - Waiting to acquire lock: lockActiveZones")
        shared.lockActiveZones.acquire()
        try:

            # If the zone is already active, skip this directive.
            if zonetimingObj.zone.id in ZoneController.activeZones:
                shared.logger.info(self, "Zone is already active")
                return True

            shared.logger.debug(self,"Adding zone '" + zonetimingObj.zone.name + "' to list of active zones")
            
            # add this zone to a list of activated zones
            

            shared.logger.debug(self,"Activating Zone")
            
            if self.zrpi_controller.activateZone(zonetimingObj.zone):
                ZoneController.activeZones[zonetimingObj.zone.id] = zonetimingObj
                result = True

        finally:
            shared.lockActiveZones.release()
            shared.logger.debug(self, "ActivateZone - releasing lock: lockActiveZones")
        
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
         
        shared.logger.debug(self, "deactivateZone - Waiting to acquire lock: lockActiveZones")
        shared.lockActiveZones.acquire()
        
        try:
            # Call the RPI controller to deactivate the zone
            self.zrpi_controller.deactivateZone(zone)

            # Remove the zone from the list of active zones
            del ZoneController.activeZones[zone.id]
        finally:
            shared.lockActiveZones.release()
            shared.logger.debug(self, "deactivateZones- releasing lock: lockActiveZones")


    def deactivateAllZones(self):
    
        shared.logger.debug(self,"Deactivating All Zones")
        shared.logger.debug(self, "deactivateAllZones - Waiting to acquire lock: lockActiveZones")
        shared.lockActiveZones.acquire()
        
        try:
            for key, activeZone in ZoneController.activeZones.items():
                shared.logger.debug(self, "Deactivating -> " + key + "-->" + activeZone.zone.name)

                #Call the RPI controller to deactivate this zone
                self.zrpi_controller.deactivateZone(zone)
            
            # Reset back to an empty hashmap
            ZoneController.activeZones = {}

        finally:
            shared.lockActiveZones.release()
            shared.logger.debug(self, "deactivateAllZones - releasing lock: lockActiveZones")

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
        # TODO: Add activation to history table
        # TODO: Tell controller to start the zone
        # return False