from service.database.db_schema import Base, Zone, TemperatureRule, Schedule
from service.database.zone_dbo import ZoneDBO
from service.utilities.conversion import Conversions
from pprint import pprint
from service.utilities.logger import Logger
from service.database.db_schema import Zone
# from service.core import shared
import sys

# TODO: consider putting in a failsafe for all zones where if they are activated for X period of time, they auto shut off.
# TODO: Consider making the auto-shutoff configurable as a system setting
# TODO: WHat do we do if pyowm can't retrieve the weather? Do we still turn on?

# This class is for managing a zone and it's information, or manipulation of the zone behavior (activation/deactivation)
class ZoneDataManager():

    # def __init__(self):
    #     self.ops = ZoneDBO()
    #     self.ops.insertRPItoPINConfig(1,10)
    
    def __init__(self):
        self.ops = ZoneDBO()
        
        # TODO: Remove this later
        self.ops.insertRPItoPINConfig( 1,10)

    # TODO: Add business logic to validate that the schedules don't overlap
    # TODO: Add business logic to disable any rules where conditions are partially populated
    # TODO: Add checkbox to UI to enable setting of the parameters
    # TODO: Add logic to check if start time < end time for all schedules
    def createZone(self, jsonData):
        shared.logger.debug(self, "ZoneManager - createZone begin")

        try:
            # # First we need to create a zone business object
            zone =  Zone.initializeWithJSON(jsonData)

            self.ops.createZone(zone)
            self.ops.saveAndClose()
            shared.logger.info(self, "Successfully added zone")
        except:
            the_type, the_value, the_traceback = sys.exc_info()
            shared.logger.error(self, "Failed to create zone")
            shared.logger.error(self, str(the_value))
            self.ops.undo()
            return False
        

        return True

    def retrieveAllZones(self):
      
        #retrieve a DO object
        zonesDO = self.ops.fetchAllZones()            
        return zonesDO

    def retrieveZone(self, zone_id):
        zoneDO = self.ops.fetchZone( zone_id)
        return zoneDO
    
    def retrieveAllEnabledZones(self):
        # zonesBO = []

        zonesDO = self.ops.fetchAllEnabledZones()
    
        return zonesDO



