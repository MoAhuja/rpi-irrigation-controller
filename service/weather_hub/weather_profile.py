

class WeatherProfile():

    def __init__(self):
        self.currentProfile = None
        self.twentyfourhourProfile = None

    def setCurrentForecast(self, forecast):
        self.currentProfile = forecast
    
    def set24HourForecast(self, forecast):
        self.twentyfourhourProfile = forecast
