
from service.rest_mappers.base_rest_mapper import BaseRestMapper
from service.system.settings_manager import SettingsManager
from service.utilities.conversion import Conversions
from service.core import shared
from datetime import datetime

class SettingsRestMapper(BaseRestMapper):

    ERROR_TYPE_NOT_VALID_DATETIME_FORMAT = "Invalid Datetime Format. Format must be YYYY-MM-DDTHH:MM:SS (e.g. 2018-07-01T00:00:40)"
    ERROR_TYPE_DATETIME_MUST_BE_FUTURE = "Invalid Datetime - Value must be in the future"
    
    GENERIC_PROPERTY_VALUE_FIELD = "value"

    FIELD_LOCATION_CITY = "city"
    FIELD_LOCATION_COUNTRY = "country"
    FIELD_RAIN_DELAY = "rain_delay"
    
    def __init__(self):
        self.smgr = SettingsManager()

    # ##################
    # Operational Settings mappers
    # ##################
    def setRainDelay(self, json_data):
        shared.logger.debug(self, "setRainDelay entered")

        # Pull the value from the rest data body
        rainDelay = json_data[self.GENERIC_PROPERTY_VALUE_FIELD]

        shared.logger.debug(self, "Rain Delay requested = " + rainDelay)

        # Must be a valid date and must be in the future
        try:
            shared.logger.debug(self, "Converting rain delay setting to date time")

            rainDelayDate = Conversions.convertRainDelaySettingToDatetime(rainDelay)
        except:
            return self.returnBadRequest(self.GENERIC_PROPERTY_VALUE_FIELD, self.ERROR_TYPE_NOT_VALID_DATETIME_FORMAT, json_data)
        

        shared.logger.debug(self, "Validating if rain delay value (" + str(rainDelayDate) + ") is set to the future.")
        
        # Check if the rain delay value is set in the past
        if rainDelayDate < datetime.now():
            shared.logger.error(self, "Rain delay set to past")
            return self.returnBadRequest(self.GENERIC_PROPERTY_VALUE_FIELD, self.ERROR_TYPE_DATETIME_MUST_BE_FUTURE, json_data)
        
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