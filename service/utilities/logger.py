from datetime import datetime
from pprint import pprint
from time import strftime
from service.database.log_dbo import LogDBO
from service.database.db_schema import EnumLogLevel
from service import shared_events
from service.system.settings_manager import SettingsManager

class Logger():

    # TODO: Change the enabled log level to a config file / db entry
    # 0 = Nothing
    # 1 ERROR
    # 2 = Info
    # 3 = Debug
    def __init__(self):
        self.consolelogLevel = -1
        self.dbLogLevel = -1
        self.dbLogger = LogDBO()
        self.settingsmanager = SettingsManager()
    
    # TODO: Add event to listen for logging level changes and update the logging level accordingly
    # shared_events.event_publisher.register(Logger, false, false, true)
    def getLogLevel(self):
        if self.consolelogLevel is -1:
            # TODO: Go to settings manager (via shared) to get log level
            self.consolelogLevel = self.settingsmanager.getConsoleLogLevel()
        
        if self.dbLogLevel is -1:
            self.dbLogLevel = self.settingsmanager.getDatabaseLogLevel()
    

    def error(self,callingClass, text):
        self.getLogLevel()
        if self.consolelogLevel > 0:
            self.internalLogger("ERROR", callingClass, text)

        if self.dbLogLevel > 0:
            self.internalDBLogger(EnumLogLevel.ERROR, callingClass, text)

    def info(self,callingClass, text):
        self.getLogLevel()
        if self.consolelogLevel > 1:
            self.internalLogger( "INFO", callingClass, text)

        if self.dbLogLevel > 1:
            self.internalDBLogger(EnumLogLevel.INFO, callingClass, text)
    
    def debug(self, callingClass, text):
        self.getLogLevel()
        if self.consolelogLevel > 2:
            self.internalLogger("DEBUG", callingClass, text)
        
        if self.dbLogLevel > 2:
            self.internalDBLogger(EnumLogLevel.DEBUG, callingClass, text)
    
    def internalLogger(self, logLevelDescription, callingClass, text):
        ts = datetime.now()
        timestring = ts.strftime("[%Y-%m-%d] [%H:%M:%S]")
        
        try:
            classString = type(callingClass).__name__
        except:
            classString = "[Unknown]"

        print(timestring + "[" + classString + "] [" + logLevelDescription + "] "  + text)


    def internalDBLogger(self, dbLogLevel, callingClass, text):
        
        try:
            classString = type(callingClass).__name__
        except:
            classString = "[Unknown]"

        self.dbLogger.logMessage(dbLogLevel, classString, text)

# TODO: threading on the db logging

        # if Logger.dbLoggingEnabled is True:
        #     