from datetime import datetime
from pprint import pprint
from time import strftime

class Logger():

    # TODO: Change the enabled log level to a config file / db entry
    # 0 = Nothin
    # 1 ERROR
    # 2 = Info
    # 3 = Debug
    logLevel = 3
    @staticmethod
    def error(callingClass, text):
        if Logger.logLevel > 0:
            Logger.internalLogger("ERROR", callingClass, text)


    @staticmethod
    def info(callingClass, text):
        if Logger.logLevel > 1:
            Logger.internalLogger("INFO", callingClass, text)

    
    @staticmethod
    def debug(callingClass, text):
        if Logger.logLevel > 2:
            Logger.internalLogger("DEBUG", callingClass, text)
    
    @staticmethod
    def internalLogger(logLevelDescription, callingClass, text):
        ts = datetime.now()
        timestring = ts.strftime("[%Y-%m-%d] [%H:%M:%S]")
        
        try:
            classString = type(callingClass).__name__
        except:
            classString = "[Unknown]"

        print(timestring + "[" + classString + "] [" + logLevelDescription + "] "  + text)