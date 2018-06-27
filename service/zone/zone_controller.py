from service.zone.zone_rpi_controller import ZoneRPIController
from service import shared
from service.utilities.logger import Logger
class ZoneController():

    zrpi_controller = None
    activeZones = {}

    def __init__(self):
        zrpi_controller = ZoneRPIController()
        activeZones = {}

        
    
    def userInvokedActivateZone(self, json_data):
        # TODO: Validate the zone is enabled
        zone_id = json_data['id']
        duration = json_data['duration']
        
        # TODO: Fetch zone using ID
        zone = self.retrieveZone(zone_id)

        # Set to current time plus the requested run time
        end_time = datetime.now() + timedelta(minute=duration)

        Logger.debug(self, "Manual Activation Requested for zone: " + zone.name + ". End time = " + str(end_time))

        # call the manual ativation function on the engine
        # shared.engine.manuallyActivateZone(zone, end_time)
        # TODO: Call new function in this class


        return False
    
    def userInvokedDeactivateZone(self, json_data):
        zone_id = json_data['id']
        
        # TODO: Fetch zone using ID
        zone = self.retrieveZone(zone_id)

        # call the manual ativation function on the engine
        shared.engine.manuallyDeactivateZone(zone)      

    def activateZone(self, zonetimingObj):

        Logger.debug(self, "ActivateZone - Waiting to acquire lock: lockActiveZones")
        shared.lockActiveZones.acquire()
        try:

            Logger.debug(self,"Adding zone '" + zone.name + "' to list of active zones")
            # add this zone to a list of activated zones
            self.activeZones[zonetimingObj.zone.id] = zonetimingObj

            Logger.debug(self,"Activating Zone")
            self.zrpi_controller.activateZone(zonetimingObj.zone)

        finally:
            shared.lockActiveZones.release()
            Logger.debug(self, "ActivateZone - releasing lock: lockActiveZones")
        

        # call the zone controller and activate the zone
        self.zone_controller.activateZone(zonetimingObj.zone)

    def deactivateZones(self, listOfKeysToDeactivate):
        
        Logger.debug(self, "deactivateZones - Waiting to acquire lock: lockActiveZones")
        shared.lockActiveZones.acquire()
        

        try:
            for x in listOfKeysToDeactivate:
                # Fetch the zonetiming object and deactivate teh zone
                self.zrpi_controller.deactivateZone(self.activateZone[x].zone)

                # Remove the zone from the list of active zones
                del self.activeZones[x]

        finally:
            shared.lockActiveZones.release()
            Logger.debug(self, "deactivateZones - releasing lock: lockActiveZones")

    def deactivateAllZones(self):
        

        Logger.debug(self,"Deactivating All Zones")
        Logger.debug(self, "deactivateAllZones - Waiting to acquire lock: lockActiveZones")
        shared.lockActiveZones.acquire()
        
        try:
            for key, activeZone in self.activeZones.items():
                Logger.debug(self, "Deactivating -> " + key + "-->" + activeZone.zone.name)

                self.zone_controller.deactivateZone(activeZone.zone)
            
            # Reset back to an empty hashmap
            self.activeZones = {}
        finally:
            shared.lockActiveZones.release()
            Logger.debug(self, "deactivateAllZones - releasing lock: lockActiveZones")

    #  def manuallyDeactivateZone(self, zone):

    #     # Check if zone is in the list of active zones
    #     if self.activeZones[zone.id] is not None:
    #         # TODO: What if a manual deactiate is called while he zone list is being?? Will this crash it?
    #         del self.activeZones[zone.id]
    #         Logger.info(self,"Zone " + str(zone.id) + "has been MANUALLY deactivated")

    #         # TODO: insert a deactivation history event
    
    # def manuallyActivateZone(self, zone, end_time):
        # TODO: Check if the zone is already active
        # TODO: This call should come from the zone manager (or some other place after validation). The user should not interface with the engine directly.
        # TODO: Inject this zone into list of active zones
        # TODO: Add decision history as "manual"
        # TODO: Add activation to history table
        # TODO: Tell controller to start the zone
        # return False