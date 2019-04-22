
from service.rest_mappers.base_rest_mapper import BaseRestMapper
from service.weather_hub.weather_center import WeatherCenter
from service.core import shared

class WeatherRestMapper(BaseRestMapper):

    FIELD_CITY = "city"
    FIELD_COUNTRY = "country"

    def __init__(self):
        self.wc = WeatherCenter()
        
    def getForecast(self, country, city):
        
        shared.logger.debug(self, "getForecast entered")
        # Get city and country
        # city = self.getKeyOrThrowException(json_data, WeatherRestMapper.FIELD_CITY, json_data)
        # country = self.getKeyOrThrowException(json_data, WeatherRestMapper.FIELD_COUNTRY, json_data)
        

        # city = self.validateIsProvidedAndString(city, WeatherRestMapper.FIELD_CITY)
        # country = self.validateIsProvidedAndString(country, WeatherRestMapper.FIELD_CITY)
        result = self.wc.createWeatherSnapshot(city, country, asJSON=True)

        print(result)
        return self.returnSuccessfulResponse(result)
        
        

    
    
    