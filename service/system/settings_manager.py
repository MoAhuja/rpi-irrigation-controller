import configparser
# from service.utilities.logger import Logger
import os
import json
from service.core import shared_events
from threading import Lock
from datetime import datetime


class SettingsManager():

    
    # operational section & fields
    section_operational = 'Operational'
    field_rain_delay = 'RainDelayInHours'

    # Logging section and fields
    section_logging = 'Logging'
    field_console_log_level = 'consoleLogLevel'
    field_database_log_level = 'databaseLogLevel'

    # Locks for each property so we don't read while a write is ongoing
    lockRainDelay = Lock()
    lockLoggingLevel = Lock()

    #Class level "asOf" date so we know if the current config is stale
    lastUpdatedDate = datetime.now()

    def __init__(self):

        print("Initializing Settings Manager")
        shared_events.event_publisher.register(self, False, False, False, True)
        # Create an instance of the config parser
        self.filePath = os.path.join(os.path.abspath(os.path.dirname(__file__)), '', 'settings.ini')
        self.config = configparser.ConfigParser()
        self.loadedConfigAsOfDate = None
        self.lock = Lock()
        self.readConfig()

    # This is the default 
    def setSettingRestMapper(self, propertyName, propertyValue):
        
        values = {}
        
        if propertyName == SettingsManager.field_console_log_level:
            self.setConsoleLogLevel(propertyValue)
        elif propertyName == SettingsManager.field_database_log_level:
            self.setDatabaseLogLevel(propertyValue)
        elif propertyName == SettingsManager.field_rain_delay:
            self.setRainDelay(propertyValue)
        values["result"] = True
        return json.dumps(values)
        
    
    def getSettingRestMapper(self, propertyName):
        
        values = {}
        if propertyName == SettingsManager.field_console_log_level:
            values["result"] = self.getConsoleLogLevel()
        elif propertyName == SettingsManager.field_database_log_level:
            values["result"] = self.getDatabaseLogLevel()
        elif propertyName == SettingsManager.field_rain_delay:
            values["result"] = self.getRainDelay()

        return json.dumps(values)

    # This event function is called by the event publisher when any logging settings are updated
    def eventSettingsUpdated(self):
        print("eventSettingsUpdated called. Going to read config")
        self.readConfig()
    
    def readConfig(self):
        print("readConfig - Acquring lock")
        self.lock.acquire()
        try:
            self.config.read(self.filePath)
        finally:
            print("readConfig - Releasing lock")
            self.lock.release()
    
    # Operational Fields
    def setRainDelay(self, hours):
        # self.readConfig()
        self.config[SettingsManager.section_operational][SettingsManager.field_rain_delay] = str(hours)
        self.save()
        shared_events.event_publisher.publishRainDelayUpdated()
    
    def getRainDelay(self):
        # self.readConfig()
        return(int(self.config[SettingsManager.section_operational][SettingsManager.field_rain_delay]))


    # Logging Fields
    def getConsoleLogLevel(self):
        # self.readConfig()
        print("getConsoleLogLevel - Acquriing lock")
        val = 0
        self.lock.acquire()
        try:
            val = int(self.config[SettingsManager.section_logging][SettingsManager.field_console_log_level])
        finally:
            print("getConsoleLogLevel - releasing lock")
            self.lock.release()

        return val
    
    def setConsoleLogLevel(self, level):
        # 0 = None, 1 = Error, 2 = Info, 3 = Debug
        self.config[SettingsManager.section_logging][SettingsManager.field_console_log_level] = str(level)
        self.save()
        shared_events.event_publisher.publishLogLevelUpdated()

        

    def getDatabaseLogLevel(self):
        # self.readConfig()
        print("getDatabaseLogLevel - Acquriing lock")
        val = 0
        self.lock.acquire()
        try:
            val = int(self.config[SettingsManager.section_logging][SettingsManager.field_database_log_level])
        finally:
            self.lock.release()
            print("getDatabaseLogLevel - releasing lock")

        return val

    def setDatabaseLogLevel(self, level):
        print("Setting database log level to: " + str(level))

        # 0 = None, 1 = Error, 2 = Info, 3 = Debug
        self.config[SettingsManager.section_logging][SettingsManager.field_database_log_level] = str(level)
        self.save()
        shared_events.event_publisher.publishLogLevelUpdated()

    def save(self):
        # self.lock.acquire()
        # try:
            with open(self.filePath, 'w') as settings_file:
                print("Updating settings.ini file")
                self.config.write(settings_file)
                settings_file.close()
                # SettingsManager.lastUpdatedDate = datetime.now()
                shared_events.event_publisher.publishSettingsUpdated()
        # finally:
        #     self.lock.release()



