
from service.rest_mappers.base_rest_mapper import BaseRestMapper
from service.system.settings_manager import SettingsManager
from service.utilities.conversion import Conversions
import json
from service.core import shared
from datetime import datetime

class SettingsRestMapper(BaseRestMapper):

    # Rain Delay Error Codes
    ERROR_TYPE_NOT_VALID_DATETIME_FORMAT = "Invalid Datetime Format. Format must be YYYY-MM-DDTHH:MM:SS (e.g. 2018-07-01T00:00:40)"
    ERROR_TYPE_DATETIME_MUST_BE_FUTURE = "Invalid Datetime - Value must be in the future"
    
    # Log Level Error Codes
    ERROR_TYPE_INVALID_LOG_LEVEL = "Log level must be between 0 - 4. 0 = Off, 1 = Error, 2 = Info, 3 = Debug"
    GENERIC_PROPERTY_VALUE_FIELD = "value"

    FIELD_LOCATION_CITY = "city"
    FIELD_LOCATION_COUNTRY = "country"
    FIELD_RAIN_DELAY = "rain_delay"
    FIELD_LOG_LEVEL = "log_level"
    FIELD_KILL_SWITCH = "kill_switch"
    FIELD_NOTIFY_START = "notify_on_watering_start"
    FIELD_NOTIFY_STOP = "notify_on_watering_stop"
    FIELD_NOTIFY_ERROR = "notify_on_error"
    
    def __init__(self):
        self.smgr = SettingsManager()

    # ####################################
    # Operational Settings mappers
    # ####################################
    
    def setConsoleLogLevel(self, json_data):
        shared.logger.debug(self, "setConsoleLogLevel entered")
        shared.logger.debug(self, "Data = " + json.dumps(json_data))
        try:
            logLevel = int(json_data[self.GENERIC_PROPERTY_VALUE_FIELD])
        except:
            self.returnBadRequest(self.GENERIC_PROPERTY_VALUE_FIELD, self.ERROR_TYPE_INVALID_VALUE, json_data)

        # Value must be 0 - 4
        if logLevel < 0 or logLevel > 4:
            self.returnBadRequest(self.GENERIC_PROPERTY_VALUE_FIELD, self.ERROR_TYPE_INVALID_LOG_LEVEL, json_data)
        else:
            self.smgr.setConsoleLogLevel(logLevel)
        

        return self.returnSuccessfulResponse()
    
    def getConsoleLogLevel(self):
        shared.logger.debug(self, "getConsoleLogLevel entered")

        try:
            logLevel = self.smgr.getConsoleLogLevel()

            response = {}
            response[self.FIELD_LOG_LEVEL] = logLevel
            return self.returnSuccessfulResponse(response)
        except:
            return self.handleSystemError()

    def setDatabaseLogLevel(self, json_data):
        shared.logger.debug(self, "setConsoleLogLevel entered")
        shared.logger.debug(self, "Data = " + json.dumps(json_data))
        
        try:
            logLevel = int(json_data[self.GENERIC_PROPERTY_VALUE_FIELD])
        except:
            self.returnBadRequest(self.GENERIC_PROPERTY_VALUE_FIELD, self.ERROR_TYPE_INVALID_VALUE, json_data)

        # Value must be 0 - 4
        if logLevel < 0 or logLevel > 4:
            self.returnBadRequest(self.GENERIC_PROPERTY_VALUE_FIELD, self.ERROR_TYPE_INVALID_LOG_LEVEL, json_data)
        else:
            self.smgr.setDatabaseLogLevel(logLevel)

        return self.returnSuccessfulResponse()
    
    def getDatabaseLogLevel(self):
        shared.logger.debug(self, "getDatabaseLogLevel entered")

        try:
            logLevel = self.smgr.getDatabaseLogLevel()

            response = {}
            response[self.FIELD_LOG_LEVEL] = logLevel
            return self.returnSuccessfulResponse(response)
        except:
            return self.handleSystemError()
    # ####################################
    # Operational Settings mappers
    # ####################################
    def setRainDelay(self, json_data):
        shared.logger.debug(self, "setRainDelay entered")
        shared.logger.debug(self, "Data = " + json.dumps(json_data))

        # Pull the value from the rest data body
        rainDelay = self.getKeyOrThrowException(json_data, self.GENERIC_PROPERTY_VALUE_FIELD, json_data)

        
        # Check if the value is null, which is allowed
        if rainDelay is None:
            result = self.smgr.setRainDelay("")
            return self.returnSuccessfulResponse()    

        shared.logger.debug(self, "Rain Delay requested = " + rainDelay)


        # Must be a valid date and must be in the future
        try:
            shared.logger.debug(self, "Converting rain delay setting to date time")
            
            rainDelayDate = Conversions.convertRainDelaySettingToDatetime(rainDelay)
        except:
            self.raiseBadRequestException(self.GENERIC_PROPERTY_VALUE_FIELD, self.ERROR_TYPE_NOT_VALID_DATETIME_FORMAT, json_data)
        

        shared.logger.debug(self, "Validating if rain delay value (" + str(rainDelayDate) + ") is set to the future.")
        
        # Check if the rain delay value is set in the past
        if rainDelayDate < datetime.now():
            shared.logger.error(self, "Rain delay set to past")
            self.raiseBadRequestException(self.GENERIC_PROPERTY_VALUE_FIELD, self.ERROR_TYPE_DATETIME_MUST_BE_FUTURE, json_data)
        
        result = self.smgr.setRainDelay(rainDelay)

        return self.returnSuccessfulResponse()

        
    def getRainDelay(self):
        shared.logger.debug(self, "getRainDelay entered")

        try:
            rainDelay = self.smgr.getRainDelay()
            shared.logger.debug(self, "Rain Delay ==" + rainDelay)

            response = {}
            response[self.FIELD_RAIN_DELAY] = rainDelay
            return self.returnSuccessfulResponse(response)
        except:
            return self.handleSystemError()


    def getLocation(self):
        response = {}
        response[self.FIELD_LOCATION_CITY] = self.smgr.getCity()
        response[self.FIELD_LOCATION_COUNTRY] = self.smgr.getCountry()
        return self.returnSuccessfulResponse(response)

    def setLocation(self, json_data):

        shared.logger.debug(self, "SetLocation Entered")
        shared.logger.debug(self, "Data = " + json.dumps(json_data))

        # Extract the two fields we care about
        city = json_data[SettingsRestMapper.FIELD_LOCATION_CITY]
        country = json_data[SettingsRestMapper.FIELD_LOCATION_COUNTRY]

        # Perform validation on the city/country
        if city is None or len(city) is 0:
            shared.logger.error(self, "City request is bad")
            return self.returnBadRequest(self.FIELD_LOCATION_CITY, BaseRestMapper.ERROR_TYPE_INVALID_VALUE, json_data)
        if country is None or len(country) is not 2:
            shared.logger.error(self, "Country request is bad")
            return self.returnBadRequest(self.FIELD_LOCATION_COUNTRY, BaseRestMapper.ERROR_TYPE_INVALID_VALUE, json_data)
        
        # Set the city and country
        # TODO: Get a more detailed response for this action
        response = self.smgr.setCity(city)
        response = self.smgr.setCountry(country)

        # return successful response
        return self.returnSuccessfulResponse()

    def setKillSwitch(self, json_data):
        
        shared.logger.debug(self, "setKillSwitch - Entered")
        shared.logger.debug(self, "Data = " + json.dumps(json_data))

        killSwitch = self.getKeyOrThrowException(json_data, SettingsRestMapper.GENERIC_PROPERTY_VALUE_FIELD, json_data)

        # Validate the kill switch is a bool
        self.validateIsProvidedAndBool(killSwitch, SettingsRestMapper.GENERIC_PROPERTY_VALUE_FIELD, json_data)

        response = self.smgr.setKillSwitch(killSwitch)
        return self.returnSuccessfulResponse()
    
    def getKillSwitch(self):
        
        response = {}
        response[self.FIELD_KILL_SWITCH] = self.smgr.getKillSwitch()
        return self.returnSuccessfulResponse(response)

    def setNotificationSettings(self, json_data):
        
        shared.logger.debug(self, "setNotificationSettings - Entered")
        shared.logger.debug(self, "Data = " + json.dumps(json_data))
        
        notifyStart = self.getKeyOrSetAsNone(json_data, SettingsRestMapper.FIELD_NOTIFY_START)
        notifyEnd = self.getKeyOrSetAsNone(json_data, SettingsRestMapper.FIELD_NOTIFY_STOP)
        notifyError = self.getKeyOrSetAsNone(json_data, SettingsRestMapper.FIELD_NOTIFY_ERROR)
        
        if notifyStart is None:
            notifyStart = False
        
        if notifyEnd is None:
            notifyEnd = False
        
        if notifyError is None:
            notifyError = False

        # Validate values are bools
        self.validateIsProvidedAndBool(notifyStart, SettingsRestMapper.FIELD_NOTIFY_START, json_data)
        self.validateIsProvidedAndBool(notifyEnd, SettingsRestMapper.FIELD_NOTIFY_STOP, json_data)
        self.validateIsProvidedAndBool(notifyError, SettingsRestMapper.FIELD_NOTIFY_ERROR, json_data)

        response = self.smgr.setAllNotificationPreferences(notifyStart, notifyEnd, notifyError)
        return self.returnSuccessfulResponse()
    
    def getNotificationSettings(self):
        
        response = {}
        # response[self.FIELD_KILL_SWITCH] = self.smgr.getKillSwitch()
        return self.returnSuccessfulResponse(response)

