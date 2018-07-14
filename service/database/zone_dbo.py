from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from service.utilities.conversion import Conversions
from service.database.base_db_operations import BaseDBOperations
from service.utilities.logger import Logger
from service.core import shared_events, shared
 
from service.database.db_schema import Base, Zone, TemperatureRule, RainRule, Schedule, RpiPinMapper
 
#Management variables
class ZoneDBO(BaseDBOperations):

    def __init__(self):
        # BaseDBOperations.__init__(self)
        self.event_pub = shared_events.event_publisher

        
    def createZone(self, zone):
        self.initialize()
        self.session.add(zone)
        self.session.flush()
    
    def deleteZone(self, zone):
        self.initialize()
        # zone = self.fetchZone(zone_id)
        self.session.delete(zone)
        self.session.flush()
    
    def editZone(self, zone_id, newZone):
        print("Zone is is --> " + str(zone_id))
        self.initialize()
        # Query the old zone
        originalZone = self.fetchZone(zone_id)
        self.session.delete(originalZone)

        self.session.flush()

        newZone.id = zone_id
        self.session.add(newZone)

        self.session.flush()

        # TODO: What if I jsut specified the ID for the zone?
        

        # if originalZone is not None:
        #     # Map all the new attributes to the original zone object
        #     originalZone.name = newZone.name
        #     originalZone.enabled = newZone.enabled
        #     originalZone.description = newZone.description

            # Update all the temperature parameters

            # Update all the rain parameters

            # Update the schedules (iterate over the lists)? Maybe just delete the schedules and re-add?
            # TODO: Do we need to return the IDs of all the schedules so they can be matched and updated accordingly?


            # cl.description=jsonData[Zone.FIELD_ZONE_NAME]
        # cl.name=jsonData[Zone.FIELD_ZONE_NAME]
        # cl.enabled=jsonData[Zone.FIELD_ENABLED]
        
        # cl.temperature = TemperatureRule.initializeWithJSON(jsonData[Zone.FIELD_TEMPERATURE], cl)
        # cl.rain = RainRule.initializeWithJSON(jsonData[Zone.FIELD_RAIN], cl)
        
        # for schedule in jsonData[Zone.FIELD_SCHEDULE]
        #     cl.schedules.append(Schedule.initializeWithJSON(schedule, cl))

        # return cl


    #     #retrieve the zone_id
    def fetchAllZones(self ):

        self.initialize()
        allZones = self.session.query(Zone).all()
        self.session.flush()
        return allZones
    
    def fetchAllEnabledZones(self):

        self.initialize()
        allZones = self.session.query(Zone).filter(Zone.enabled==True).all()
        self.session.flush()
        return allZones
    
    def fetchZone(self, zone_id):
        self.initialize()
        print("Fetching zone by id:" + str(zone_id))

        zoneDO = self.session.query(Zone).filter(Zone.id==zone_id).first()
        self.session.flush()
        return zoneDO

    def fetchZoneByName(self, zone_name):
        self.initialize()
        zoneDO = self.session.query(Zone).filter(Zone.name==zone_name).first()
        self.session.flush()
        return zoneDO


    def insertRPItoPINConfig(self, relay_id, rpi_pin):
        self.initialize()
    
        pin_config = self.session.query(RpiPinMapper).filter_by(relay_id=relay_id).first()
        if pin_config:
            return pin_config
        else:
            pin_config = pin_config = RpiPinMapper(relay_id=relay_id, rpi_pin=rpi_pin)
            self.session.add(pin_config)
            self.session.flush()
            return pin_config
    
    
    def mapZoneToRelay(self, zone_id, relay_id):
        self.initialize()

        relay = self.session.query(RpiPinMapper).filter_by(relay_id=relay_id).first()  # @note: code is Integer, not a String, right?
        if relay:
            relay.zone_id = zone_id
            self.session.add(relay)
            self.session.flush()
            
    def saveAndClose(self):
        # call the base class to save the changes
        if super(ZoneDBO, self).saveAndClose():
            self.event_pub.publishZoneInfoUpdated()
            shared.logger.debug(self, "Zone information saved")
            return True
        else:
            shared.logger.error(self, "Zone information not saved")
            return False

        return False
        # Call the event manager to notify of a change
        

  



