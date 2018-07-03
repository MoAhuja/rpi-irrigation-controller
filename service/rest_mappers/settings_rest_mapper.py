
from service.rest_mappers.base_rest_mapper import BaseRestMapper
from service.system.settings_manager import SettingsManager
from service.core import shared

class SettingsRestMapper(BaseRestMapper):

    GENERIC_PROPERTY_VALUE_FIELD = "value"

    FIELD_LOCATION_CITY = "city"
    FIELD_LOCATION_COUNTRY = "country"

    def __init__(self):
        self.smgr = SettingsManager()

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