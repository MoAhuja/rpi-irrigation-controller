from datetime import datetime, time, timezone
from time import gmtime, strftime
# from service.utilities.logger import Logger

class Conversions():
    rainDelayFormat = "%Y-%m-%dT%H:%M:%S"

    @staticmethod
    def __init__():
        self.humanReadableDatePattern = ""
    
    @staticmethod
    def utc_to_local(utc_dt):
        return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

    @staticmethod
    def convertDBTimeToHumanReadableTime(time_object):
        return time_object.strftime("%H:%M")
    
    @staticmethod
    def convertHumanReadableTimetoDBTime(stringTime):
        return datetime.strptime(stringTime, '%H:%M').time()
    
    @staticmethod
    def convertDateTimeToString(datetime):
        return datetime.strftime(Conversions.rainDelayFormat)
    
    @staticmethod
    def convertRainDelaySettingToDatetime(rainDelayAsString):
        return datetime.strptime(rainDelayAsString, Conversions.rainDelayFormat)
        
    
    @staticmethod
    def printVarsInObject(objectToPrint):
        attrs = vars(objectToPrint)
        # {'kids': 0, 'name': 'Dog', 'color': 'Spotted', 'age': 10, 'legs': 2, 'smell': 'Alot'}
        # now dump this in some way or another
        print (', '.join("%s: %s" % item for item in attrs.items()))