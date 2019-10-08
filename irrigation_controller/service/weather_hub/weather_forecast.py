from pprint import pprint

class WeatherForecast():

    FIELD_TEMP = "temperature"
    FIELD_WIND_SPEED = "wind_speed"
    FIELD_RAIN_AMOUNT = "rain_amount"

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
    
    def toDictionary(self):
        myDict = {}
        myDict[WeatherForecast.FIELD_RAIN_AMOUNT] = self.getRainAmount()
        myDict[WeatherForecast.FIELD_TEMP] = self.getTemperature().toDictionary()
        myDict[WeatherForecast.FIELD_WIND_SPEED] = self.getMaxWindSpeed()
        return myDict
    

class Temperature():

    def __init__(self):
        self.current = 0
        self.min = 0
        self.max = 0
    
    def __init__(self, tempStruct):
        self.current = tempStruct['temp']
        self.min = tempStruct['temp_min']
        self.max = tempStruct['temp_max']
    
    def toDictionary(self):
        myDict = {}
        myDict["current"] = self.current
        myDict["min"] = self.min
        myDict["max"] = self.max
        return myDict




