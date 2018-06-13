from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from service.utilities.conversion import Conversions
from service.database.base_db_operations import BaseDBOperations
from service.utilities.logger import Logger
 
from service.database.db_schema import Base, Zone, TemperatureRule, RainRule, Schedule, RpiPinMapper
 
#Management variables
class ZoneDBO(BaseDBOperations):

    def __init__(self, event_publisher):
        # BaseDBOperations.__init__(self)
        self.event_pub = event_publisher

    def insertTemperatureRule(self, zone_id, lower_limit, upper_limit, enabled):
        #initialize
        self.initialize()
        temp_rule = TemperatureRule(zone_id=zone_id, lower_limit=lower_limit, upper_limit=upper_limit, enabled=enabled)
        self.session.add(temp_rule)
        self.session.flush()
        
        return temp_rule.id


    def insertRainRule(self, zone_id, short_term_limit, daily_limit, enabled):
        #initialize
        self.initialize()
        rain_rule = RainRule(zone_id=zone_id, short_term_limit=short_term_limit, daily_limit=daily_limit, enabled=enabled)
        self.session.add(rain_rule)
        self.session.flush()
        
        return rain_rule.id

    def insertZone(self, name, description):
        #initialize
        self.initialize()
        zone = Zone(name=name, description=description)
        self.session.add(zone)
        self.session.flush()

        return zone.id

    def insertSchedule(self,zone_id, startTime, endTime, enabled):
        
        self.initialize()
        schedule = Schedule(zone_id=zone_id, start_time=startTime, end_time=endTime, enabled=enabled)
        self.session.add(schedule)
        self.session.flush()

        return schedule.id
        
        #retrieve the zone_id
    def fetchAllZones(self ):

        self.initialize()
        allZones = self.session.query(Zone).all()
        return allZones
    
    def fetchAllEnabledZones(self):

        self.initialize()
        allZones = self.session.query(Zone).filter(Zone.enabled==True).all()
        return allZones
    
    def fetchZone(self, zone_id):
        self.initialize()
        zoneDO = self.session.query(Zone).filter(Zone.id==zone_id).first()
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
            Logger.debug(self, "Zone information saved")
            return True
        else:
            Logger.error(self, "Zone information not saved")
            return False

        return False
        # Call the event manager to notify of a change
        

  



