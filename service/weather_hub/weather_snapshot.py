

class WeatherSnapshot():

    FIELD_CURRENT_FORECAST = "short_term_forecast"
    FIELD_DAILY_FORECAST = "daily_forecast"
    def __init__(self):
        self.currentForecast = None
        self.twentyfourhourForecast = None

    def setCurrentForecast(self, forecast):
        self.currentForecast = forecast
    
    def set24HourForecast(self, forecast):
        self.twentyfourhourForecast = forecast
    
    def toDictionary(self):
        myDict = {}
        myDict[WeatherSnapshot.FIELD_CURRENT_FORECAST] = self.currentForecast.toDictionary()
        myDict[WeatherSnapshot.FIELD_DAILY_FORECAST] = self.twentyfourhourForecast.toDictionary()
        return myDict
        

