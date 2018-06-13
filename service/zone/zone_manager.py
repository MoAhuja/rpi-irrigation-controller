from service.zone.zone_bo import ZoneBO

from service.database.db_schema import Base, Zone, TemperatureRule, Schedule
from service.database.zone_dbo import ZoneDBO
from service.utilities.conversion import Conversions
from pprint import pprint
from service.utilities.logger import Logger
import sys
# TODO: consider putting in a failsafe for all zones where if they are activated for X period of time, they auto shut off.
# TODO: Consider making the auto-shutoff configurable as a system setting
# TODO: WHat do we do if pyowm can't retrieve the weather? Do we still turn on?

# This class is for managing a zone and it's information. 
class ZoneManager():

    # def __init__(self):
    #     self.ops = ZoneDBO()
    #     self.ops.insertRPItoPINConfig(1,10)
    
    def __init__(self, event_publisher):
        self.ops = ZoneDBO(event_publisher)
        
        # TODO: Remove this later
        self.ops.insertRPItoPINConfig( 1,10)

    # TODO: Add business logic to validate that the schedules don't overlap
    # TODO: Add business logic to disable any rules where conditions are partially populated
    # TODO: Add checkbox to UI to enable setting of the parameters
    # TODO: Add logic to check if start time < end time for all schedules
    def createZone(self, jsonData):
        Logger.debug(self, "ZoneManager - createZone begin")

        try:
            # First we need to create a zone business object
            zoneBO =  ZoneBO.initializeWithJSON(jsonData)
            # pprint(vars(zoneBO))

            # Create the zone
            zoneID = self.ops.insertZone( zoneBO.zone_name, zoneBO.zone_description)
            # pprint("Zone ID == " + str(zoneID))

            # create the temperature rule
            temperatureID = self.ops.insertTemperatureRule( zoneID, zoneBO.temperature.lower_limit, zoneBO.temperature.upper_limit, zoneBO.temperature.enabled)
            # pprint("Temperature ID == " + str(temperatureID))

            #create rain rule
            rainID = self.ops.insertRainRule( zoneID, zoneBO.rain.threeHourLimit, zoneBO.rain.fullDayLimit, zoneBO.rain.enabled)
            # pprint("Rain ID == " + str(rainID))

            # TODO: Remove this and make it dynamic
            pin_config = self.ops.mapZoneToRelay( zoneID, 1)

            for sch in zoneBO.schedule:
                schID = self.ops.insertSchedule( zoneID, sch.getStartDBTime(), sch.getEndDBTime(), sch.enabled)
                # pprint("Schedule ID == " + str(schID))

            self.ops.saveAndClose()
            Logger.info(self, "Successfully added zone")
        except:
            the_type, the_value, the_traceback = sys.exc_info()
            Logger.error(self, "Failed to create zone")
            Logger.error(self, str(the_value))
            self.ops.undo()
            return False
        

        return True

    def retrieveAllZones(self):
      
        #retrieve a DO object
        zonesBO = []

        zonesDO = self.ops.fetchAllZones()

        for zone in zonesDO:
            bo = ZoneBO.initializeWithZoneDO(zone)
            zonesBO.append(bo)
            
        return zonesBO

    def retrieveZone(self, zone_id):
        zoneDO = self.ops.fetchZone( zone_id)
        zoneBO = ZoneBO.initializeWithZoneDO(zoneDO)
        return zoneBO
    
    def retrieveAllEnabledZones(self):
        zonesBO = []

        zonesDO = self.ops.fetchAllEnabledZones()

        for zone in zonesDO:
            bo = ZoneBO.initializeWithZoneDO(zone)
            zonesBO.append(bo)
            
        return zonesBO

        #normalize to a BO object
    # def deleteZone(id?)
    # def editZone(id, jsonData) -- Need to figure out how to find assoicated objects and update them?
    # def fetchZone(id):


