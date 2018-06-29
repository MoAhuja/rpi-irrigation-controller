import configparser
# from service.utilities.logger import Logger
import os
from service import shared_events
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

        # Create an instance of the config parser
        self.filePath = os.path.join(os.path.abspath(os.path.dirname(__file__)), '', 'settings.ini')
        self.config = configparser.ConfigParser()
        self.loadedConfigAsOfDate = None
        self.readConfig()
    
    def readConfig(self):
        # from service import shared as x
        # x.logger.debug(self, "Settings.ini was last updated as of: " + str(lastUpdatedDate))
        # x.logger.debug(self, "Instance of config was last loaded: " + str(loadedConfigAsOfDate))
        # TODO: Make this event driven instead of checking each time
        print("Settings.ini was last updated as of: " + str(SettingsManager.lastUpdatedDate))
        print("Instance of config was last loaded: " + str(self.loadedConfigAsOfDate))

        if self.loadedConfigAsOfDate is None or self.loadedConfigAsOfDate < SettingsManager.lastUpdatedDate:
            print("Going to load fresh config")
            self.config.read(self.filePath)
            self.loadedConfigAsOfDate = SettingsManager.lastUpdatedDate
    
    # Operational Fields
    def setRainDelay(self, hours):
        self.readConfig()
        self.config[SettingsManager.section_operational][SettingsManager.field_rain_delay] = str(hours)
        self.save()
        shared_events.event_publisher.publishRainDelayUpdated()
    
    def getRainDelay(self):
        self.readConfig()
        return(int(self.config[SettingsManager.section_operational][SettingsManager.field_rain_delay]))


    # Logging Fields
    def getConsoleLogLevel(self):
        self.readConfig()
        return(int(self.config[SettingsManager.section_logging][SettingsManager.field_console_log_level]))

    def getDatabaseLogLevel(self):
        self.readConfig()
        return(int(self.config[SettingsManager.section_logging][SettingsManager.field_database_log_level]))
        

    def save(self):
        with open(self.filePath, 'w') as settings_file:
            print("Updating settings.ini file")
            self.config.write(settings_file)
            SettingsManager.lastUpdatedDate = datetime.now()



