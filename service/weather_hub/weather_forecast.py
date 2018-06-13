from pprint import pprint

class WeatherForecast():

    def __init__(self):
        self.temperature = None
        self.wind = 0
        self.rainAmount = 0

    def setTemperature(temp):
        self.temperature = temp
    
    def setMaxWindSpeed(self, windSpeed):
        self.windSpeed = windSpeed
    
    def getTemperature(self):
        return self.temperature

    def getMaxWindSpeed(self):
        return self.windSpeed
    
    def setRainAmount(self, amount):
        self.rainAmount = amount
    
    def getRainAmount(self):
        return self.rainAmount
    
    # Parsing from struct #
    def setTempFromStruct(self, tempStruct):
        # print ("Setting temp frmo struct")
        self.temperature = Temperature(tempStruct)
        # pprint(vars(self.temperature))
    

class Temperature():

    def __init__(self):
        self.current = 0
        self.min = 0
        self.max = 0
    
    def __init__(self, tempStruct):
        self.current = tempStruct['temp']
        self.min = tempStruct['temp_min']
        self.max = tempStruct['temp_max']




