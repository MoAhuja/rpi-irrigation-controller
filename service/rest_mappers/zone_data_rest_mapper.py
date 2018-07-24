
from service.rest_mappers.base_rest_mapper import BaseRestMapper
import json
from flask import jsonify
from service.utilities.conversion import Conversions
from service.database.db_schema import EnumScheduleType, Zone, TemperatureRule, RainRule, Schedule
from service.zone.zone_data_manager import ZoneDataManager
from service.core import shared
import sys

class ZoneDataRestMapper(BaseRestMapper):


    def __init__(self):
        self.zdm = ZoneDataManager()

    # Logic errors
    ERROR_TYPE_MIN_NOT_BELOW_MAX = "Invalid Value - Temperature Min must be below temperature max"
    ERROR_TYPE_INVALID_TIME = "Invalid Value - Time must be formatted as HH:MM"
    ERROR_TYPE_INVALID_SCHEDULE_TYPE = "Invalid Value - Schedule type must be one of [" + str(EnumScheduleType.DayAndTime.value) + "," + str(EnumScheduleType.TimeAndFrequency.value) + "]"
    ERROR_TYPE_INVALID_DAY_TYPE = "Invalid Value - Days must range between 0 and 6"
    ERROR_TYPE_ZONE_NAME_MUST_BE_UNIQUE = "Zone name already exists"
    ERROR_TYPE_ZONE_ID_NOT_FOUND = "Zone ID not found"
    
    def getZone(self, zone_id):
        
        # Check if the zone exists
        zone = self.zdm.retrieveZone(zone_id, True)

        if zone is None:
            self.raiseBadRequestException(Zone.FIELD_ID, ZoneDataRestMapper.ERROR_TYPE_ZONE_ID_NOT_FOUND)

        return json.dumps(zone)
    
    def deleteZone(self, zone_id):
        
        # Validate the zone_id
        self.validateIsProvidedAndInt(zone_id, Zone.FIELD_ID)

        zone = self.zdm.retrieveZone(zone_id, False)

        if zone is None:
            self.raiseBadRequestException(Zone.FIELD_ID, ZoneDataRestMapper.ERROR_TYPE_ZONE_ID_NOT_FOUND)


        # Delete the zone
        self.zdm.deleteZone(zone)

        return self.returnSuccessfulResponse()

    def editZone(self, json_data):
        # Get an ID
        zone_id = self.getKeyOrThrowException(json_data, Zone.FIELD_ID, json_data)
        shared.logger.debug(self, "Edit Zone Called for ZOne --> " + str(zone_id))

        # Validate all the data
        newZone = self.validateDataAndCreateZoneObject(json_data, zone_id)

         # Get the relay ID if it's provided
        relay_id = self.getKeyOrSetAsNone(json_data, Zone.FIELD_RELAY)


        # Edit the zone
        result = self.zdm.editZone(zone_id, newZone, relay_id=relay_id)

        if result is True:
            shared.logger.info(self, "Successfully edited zone")
            return self.returnSuccessfulResponse()
        else:
            self.raiseServerErrorException()


    def createZone(self, json_data):
        shared.logger.debug(self, "ZoneManager - create zone")

        zone = self.validateDataAndCreateZoneObject(json_data)
        # Get the relay ID if it's provided
        relay_id = self.getKeyOrSetAsNone(json_data, Zone.FIELD_RELAY)


        result = self.zdm.createZone(zone, relay_id)

        
        # TODO: Create zone needs to be extended to return specific errors based on integrity checks?
        if result is True:
            shared.logger.info(self, "Successfully added zone")
            return self.returnSuccessfulResponse()
        else:
            self.raiseServerErrorException()
        
    def validateDataAndCreateZoneObject(self, json_data, zone_id=None):

        # TODO: Add business logic to validate that the schedules don't overlap
        # TODO: Add logic to check if start time < end time for all schedules
    
        #Enabled
        zone_enabled = self.getKeyOrThrowException(json_data, Zone.FIELD_ENABLED, json_data)
        self.validateIsProvidedAndBool(zone_enabled, Zone.FIELD_ENABLED, json_data)
        
        # Check zone name
        zone_name = self.getKeyOrThrowException(json_data, Zone.FIELD_ZONE_NAME, json_data)
        self.validateIsProvidedAndString(zone_name, Zone.FIELD_ZONE_NAME, json_data)

        # Check if the name already exists
        originalZone = self.zdm.getZoneByName(zone_name)

        if originalZone is not None:

            # Check if the ID is the same as the ID collected (meaning we're trying to create a new object)
            if zone_id != originalZone.id:
                self.raiseBadRequestException(Zone.FIELD_ZONE_NAME, self.ERROR_TYPE_ZONE_NAME_MUST_BE_UNIQUE, json_data)
        
        
        # Check zone description
        zone_description = self.getKeyOrThrowException(json_data, Zone.FIELD_ZONE_DESCRIPTION, json_data)
        self.validateIsProvidedAndString(zone_description, Zone.FIELD_ZONE_DESCRIPTION, json_data)
        
        # ###################
        # Temperature Validations
        #####################
        temperature_rule_enabled = self.getKeyOrThrowException(json_data[TemperatureRule.FIELD_TEMPERATURE],TemperatureRule.FIELD_ENABLED, json_data)
        
        # Check to make sure the data type of the enabled flag is set correctly
        self.validateIsProvidedAndBool(temperature_rule_enabled, Zone.FIELD_ENABLED, json_data)
        
        if temperature_rule_enabled is True:
            # Validate the min and max are provided
            temp_min = self.getKeyOrThrowException(json_data[TemperatureRule.FIELD_TEMPERATURE],TemperatureRule.FIELD_TEMPERATURE_MIN, json_data)
            temp_max = self.getKeyOrThrowException(json_data[TemperatureRule.FIELD_TEMPERATURE],TemperatureRule.FIELD_TEMPERATURE_MAX, json_data)


            temp_min=self.validateIsProvidedAndInt(temp_min, TemperatureRule.FIELD_TEMPERATURE_MIN, json_data)
            temp_max=self.validateIsProvidedAndInt(temp_max, TemperatureRule.FIELD_TEMPERATURE_MAX, json_data)

            # Validate the min and max don't cross
            if temp_min >= temp_max:
                self.raiseBadRequestException(TemperatureRule.FIELD_TEMPERATURE_MIN, self.ERROR_TYPE_MIN_NOT_BELOW_MAX, json_data, temp_min)

        # #######################
        # Rain Validations
        # #######################
        rain_rule_enabled = self.getKeyOrThrowException(json_data[RainRule.FIELD_RAIN],RainRule.FIELD_ENABLED, json_data)
        
        self.validateIsProvidedAndBool(rain_rule_enabled,RainRule.FIELD_ENABLED, json_data)

        if rain_rule_enabled is True:
            rain_short_term_limit = self.getKeyOrThrowException(json_data[RainRule.FIELD_RAIN],RainRule.FIELD_RAIN_SHORT_TERM_LIMIT, json_data)
            rain_daily_limit = self.getKeyOrThrowException(json_data[RainRule.FIELD_RAIN],RainRule.FIELD_RAIN_DAILY_LIMIT, json_data)

            rain_short_term_limit = self.validateIsProvidedAndInt(rain_short_term_limit, RainRule.FIELD_RAIN_SHORT_TERM_LIMIT, json_data)
            rain_daily_limit= self.validateIsProvidedAndInt(rain_daily_limit, RainRule.FIELD_RAIN_DAILY_LIMIT, json_data)

        # #######################
        # Validate Schedules
        # #######################
        schedules = self.getKeyOrThrowException(json_data, Schedule.FIELD_SCHEDULE, json_data)

        # Validate each schedule
        for schedule in schedules:

            enabled = self.getKeyOrThrowException(schedule ,Schedule.FIELD_ENABLED, json_data)
            start_time = self.getKeyOrThrowException(schedule, Schedule.FIELD_SCHEDULE_START_TIME, json_data)
            end_time = self.getKeyOrThrowException(schedule, Schedule.FIELD_SCHEDULE_END_TIME, json_data)
            schedule_type = self.getKeyOrThrowException(schedule,Schedule.FIELD_SCHEDULE_TYPE, json_data)
            days = self.getKeyOrThrowException(schedule,Schedule.FIELD_SCHEDULE_DAYS, json_data)

            # Validate enabled
            self.validateIsProvidedAndBool(enabled, Schedule.FIELD_ENABLED, json_data)
            
            # Validate schedule type
            schedule_type = self.validateIsProvidedAndInt(schedule_type, Schedule.FIELD_SCHEDULE_TYPE, json_data)
            # TODO:Validate it falls within 0,1 
            # Validate times
            self.validateIsProvidedAndString(start_time, Schedule.FIELD_SCHEDULE_START_TIME, json_data)
            self.validateIsProvidedAndString(end_time, Schedule.FIELD_SCHEDULE_END_TIME, json_data)

            try:
                Conversions.convertHumanReadableTimetoDBTime(start_time)
            except:
                self.raiseBadRequestException(Schedule.FIELD_SCHEDULE_START_TIME, self.ERROR_TYPE_INVALID_TIME,json_data, start_time)

            try:
                Conversions.convertHumanReadableTimetoDBTime(end_time)
            except:
                self.raiseBadRequestException(Schedule.FIELD_SCHEDULE_END_TIME, self.ERROR_TYPE_INVALID_TIME,json_data, end_time)

            # Validate schedule type
            self.validateIsProvidedAndInt(schedule_type, Schedule.FIELD_SCHEDULE_TYPE, json_data)
            
            if schedule_type not in [EnumScheduleType.DayAndTime.value, EnumScheduleType.TimeAndFrequency.value]:
                self.raiseBadRequestException(Schedule.FIELD_SCHEDULE_TYPE, self.ERROR_TYPE_INVALID_SCHEDULE_TYPE, json_data, schedule_type)

            # Validate days
            for day in days:
                day = self.validateIsProvidedAndInt(day, Schedule.FIELD_SCHEDULE_DAYS, json_data)
                if day <0 or day >6:
                    self.raiseBadRequestException(Schedule.FIELD_SCHEDULE_DAYS, self.ERROR_TYPE_INVALID_DAY_TYPE, json_data, day)

        # # First we need to create a zone business object
        zone =  Zone.initializeWithJSON(json_data)

        return zone

    def getAllZones(self):
        allZones = self.zdm.retrieveAllZones(True)
        return json.dumps(allZones)

