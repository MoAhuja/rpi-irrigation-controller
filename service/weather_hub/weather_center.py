import pyowm
from service.weather_hub.weather_snapshot import WeatherSnapshot
from service.weather_hub.weather_forecast import WeatherForecast
from service.core import shared
from pprint import pprint

class WeatherCenter():

    owm = None

    def __init__(self):
        if self.owm is None:
            #self.owm = pyowm.OWM('46994039d0ee54eb08eeb19503e37a9c')
            self.owm = pyowm.OWM('doesNotExist')

    # Create a weather snapshot of a 3 hour and daily forecast
    def createWeatherSnapshot(self, city, country, asJSON=False):

        shared.logger.debug(self, "Creating weather snapshot for [" + country + "]")
        # Create the objec to hold the short and long term forecast
        snapshot = WeatherSnapshot()
        
        try:
        # Create a forecaster object for the city and country provided
            forecasterObj = self.owm.three_hours_forecast(city + "," + country).get_forecast()
            dailyForecast = self.getDailyForecast(forecasterObj)
            snapshot.set24HourForecast(dailyForecast)
        
            # Get the short term forecast
            currentForecast = self.getCurrentForecast(forecasterObj)
            snapshot.setCurrentForecast(currentForecast)
        except:
            shared.logger.error(self, "Failed to get forecast. Going to create forecast with no rain.")
        # Get the daily forecast
        

        if(asJSON):
            # Convert the snapshot to a dictrionary
            return snapshot.toDictionary()
        else:
            return snapshot

    # Daily Forecast = 24 hours
    def getDailyForecast(self, forecastObj):
        
        #Get the full forecast (1 days, 3 hour intervals = 8 iterations)
        dailyForecast = self.createAggregateForcastFromForecastObject(8, forecastObj)
        return dailyForecast

    # Current forecast = 3 hours
    def getCurrentForecast(self, forecastObj):
        currentForecast = self.createAggregateForcastFromForecastObject(1, forecastObj)
        return currentForecast
    

    def createAggregateForcastFromForecastObject(self, numberOfIntervals,forecastObj):
        
        weathers = forecastObj.get_weathers()

        total_rain_amount = 0
        max_wind = 0
        total_temp_struct = weathers[0].get_temperature('celsius')

        # print("Number of waether objects -->" + str(len(weathers)))
        # print("Number of intervals --> " + str(numberOfIntervals))

        # If we have a sufficient number of weather objects
        if(numberOfIntervals <= len(weathers)):
            count = 0
            while(count < numberOfIntervals):
                # If there is rain, add it to the total
                rain_struct = weathers[count].get_rain()
                # print(rain_struct)
                # print(rain_struct)
                if('3h' in rain_struct):
                    total_rain_amount = total_rain_amount + rain_struct['3h']

                # Get the maximum wind speed for this interval
                wind_struct = weathers[count].get_wind()
                max_wind = self.getMax(max_wind, wind_struct['speed'])

                #Get the highest and lowest temperature int he interval
                temp_struct = weathers[count].get_temperature('celsius')
                total_temp_struct['temp_max'] = self.getMax(total_temp_struct['temp_max'], temp_struct['temp_max'])
                total_temp_struct['temp_min'] = self.getMin(total_temp_struct['temp_min'], temp_struct['temp_min'])
            
                count = count + 1

            #Create and return a weather forecast object
            forecast = WeatherForecast()
            forecast.setRainAmount(total_rain_amount)
            forecast.setMaxWindSpeed(max_wind)
            forecast.setTempFromStruct(total_temp_struct)

            # pprint(vars(forecast))

            return forecast

        else:
            print("not okay")
        
        return None

        
        

    def getMax(self, existingMax, currentValue):
        if(currentValue > existingMax):
            return currentValue
        else:
            return existingMax

    def getMin(self, existingMin, currentValue):
        if(currentValue < existingMin):
            return currentValue
        else:
            return existingMin


        # wind_struct = weather.get_wind()
        # rain_struct = weather.get_rain()
        # detailed_weather = weather.get_detailed_status()
    


