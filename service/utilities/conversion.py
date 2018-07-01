from datetime import datetime, time
from time import gmtime, strftime
# from service.utilities.logger import Logger

class Conversions():
    rainDelayFormat = "%Y-%m-%dT%H:%M:%S"

    @staticmethod
    def __init__():
        self.humanReadableDatePattern = ""
    
    @staticmethod
    def convertDBTimeToHumanReadableTime(time_object):
        return time_object.strftime("%H:%M")
    
    @staticmethod
    def convertHumanReadableTimetoDBTime(stringTime):
        return datetime.strptime(stringTime, '%H:%M').time()
    
    @staticmethod
    def convertRainDelayDateTimeToString(datetime):
        return ""
    
    @staticmethod
    def convertRainDelaySettingToDatetime(rainDelayAsString):
        return datetime.strptime(rainDelayAsString, Conversions.rainDelayFormat)
        
    
    @staticmethod
    def printVarsInObject(objectToPrint):
        attrs = vars(objectToPrint)
        # {'kids': 0, 'name': 'Dog', 'color': 'Spotted', 'age': 10, 'legs': 2, 'smell': 'Alot'}
        # now dump this in some way or another
        print (', '.join("%s: %s" % item for item in attrs.items()))