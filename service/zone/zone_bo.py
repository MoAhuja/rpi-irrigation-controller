import json
from pprint import pprint
from collections import namedtuple
from service.database.db_schema import Zone, Schedule, RainRule, TemperatureRule
from service.utilities.conversion import Conversions

# The zoneBO is the non-database centric version of the zone object. It is what is passed throughout
# the application to represent a zone and the associated fields
class ZoneBO():


    
    def __init__(self):
        # print("ZoneBO - Init")
        self.zone_description=""
        self.zone_name=""
        self.zone_enabled=False
        self.temperature = None
        self.rain = None
        self.pin_config = None
        self.schedule = []
    
    @classmethod
    def initializeWithJSON(cls, jsonData):

        cl = cls()

        # SCH = namedtuple('startTime', 'endTime')
        # print("ZoneBO - with JSON Data called")
        cl.zone_description=jsonData["input_zone_description"]
        cl.zone_name=jsonData["input_zone_name"]
        cl.zone_enabled=True
        cl.temperature = TemperatureBO.initializeWithJSON(jsonData["temperature"])
        cl.rain = RainBO.initializeWithJSON(jsonData["rain"])
        cl.schedule = []
        for schedule in jsonData["schedule"]:
            cl.schedule.append(ScheduleBO.initializeWithTimes(schedule["startTime"], schedule["endTime"]))
        
        return cl
    
    @classmethod
    def initializeWithZoneDO(cls, zone_do):
        
        cl = cls()
        cl.zone_name = zone_do.name
        cl.zone_description = zone_do.description
        cl.zone_enabled = zone_do.enabled
        cl.temperature = TemperatureBO.initializeWithTemperatureDO(zone_do.temperature_rule)
        cl.rain = RainBO.initializeWithRainDO(zone_do.rain_rule)
        cl.schedule = []
        cl.pin_config = PINConfig.initializeWithPINMapperDO(zone_do.pin_config)
        for sch in zone_do.schedules:
            # print("Adding zone schedule")
            sc_bo = ScheduleBO.initializeWithScheduleDO(sch)
            cl.schedule.append(sc_bo)

        return cl
       

class TemperatureBO():
    def __init__(self):
        # print ("temperature bo init")
        self.lower_limit = 0
        self.upper_limit = 0
        self.enabled = False
    
    @classmethod
    def initializeWithJSON(cls, jsonData):
        cl = cls()
        # print ("temperature bo init with JSON")
        # Validate the data first, if good assign
        cl.lower_limit = jsonData["min"]
        cl.upper_limit = jsonData["max"]
        cl.enabled = True

        return cl
    
    @classmethod
    def initializeWithTemperatureDO(cls, temp_do):
        cl = cls()

        if temp_do is not None:
            cl.lower_limit = temp_do.lower_limit
            cl.upper_limit = temp_do.upper_limit
            cl.enabled = temp_do.enabled

        return cl

class RainBO():
    
    def __init__(self):
        self.threeHourLimit = 0
        self.fullDayLimit = 0
        self.enabled = False

    @classmethod
    def initializeWithJSON(cls, jsonData):
        cl = cls()
        cl.threeHourLimit = jsonData["shortTermExpectedRain"]
        cl.fullDayLimit = jsonData["dailyExpectedRainAmount"]
        cl.enabled = True

        return cl
    

    @classmethod
    def initializeWithRainDO(cls, rain_do):
        cl = cls()
        if rain_do is not None:
            cl.threeHourLimit = rain_do.short_term_limit
            cl.fullDayLimit = rain_do.daily_limit
            cl.enabled = rain_do.enabled
        
        return cl


class ScheduleBO():
    start = 0
    stop = 0
    enabled = False

    def __init__(self):
        self.start = 0
        self.stop = 0
        self.enabled = False
    
    @classmethod
    def initializeWithTimes(cls, iStart, iStop):
        cl = cls()
        # print("Creating schedule DO")
        cl.start = iStart
        cl.stop = iStop
        cl.enabled = True

        return cl
    
    @classmethod
    def initializeWithScheduleDO(cls, schedule_do):
        cl = cls()

        cl.start = Conversions.convertDBTimeToHumanReadableTime(schedule_do.start_time)
        cl.stop = Conversions.convertDBTimeToHumanReadableTime(schedule_do.end_time)
        cl.enabled = schedule_do.enabled

        return cl
    
    def getStartDBTime(self):
        # Convert to DB time
        return Conversions.convertHumanReadableTimetoDBTime(self.start)
    
    def getEndDBTime(self):
        return Conversions.convertHumanReadableTimetoDBTime(self.stop)

class PINConfig():

    def __init__(self):
        self.relay_id = 0
        self.rpi_pin = 0

    @classmethod
    def initializeWithPINMapperDO(cls, pin_config_do):
        cl = cls()
        if pin_config_do is not None:
            cl.relay_id = pin_config_do.relay_id
            cl.rpi_pin = pin_config_do.rpi_pin
        return cl