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

    
    def createZone(self, zone):
        self.ops.createZone(zone)
        return self.ops.saveAndClose()
    
    def editZone(self, zone_id, zone):
        self.ops.editZone(zone_id, zone)
        return self.ops.saveAndClose()

    # TODO: normalize all these names (retrieve vs get)
    def retrieveAllZones(self, asJSON=False):
      
        #retrieve a DO object
        zonesDO = self.ops.fetchAllZones()   

        if asJSON is True:
            jsonDict =  []
            for zone in zonesDO:
                jsonDict.append(zone.toDictionary())
            return jsonDict   
        else:         
            return zonesDO

    def retrieveZone(self, zone_id, asJSON=False):
        zoneDO = self.ops.fetchZone( zone_id)

        if asJSON is True:
            return zoneDO.toDictionary()
        
        return zoneDO
    
    def retrieveAllEnabledZones(self, asJSON=False):
        # zonesBO = []

        zonesDO = self.ops.fetchAllEnabledZones()
    
        return zonesDO
    
    def getZoneByName(self, zone_name):
        return self.ops.fetchZoneByName(zone_name)
    



