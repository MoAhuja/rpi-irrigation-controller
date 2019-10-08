import configparser
import os
from service.core import shared_events
from threading import Lock
from datetime import datetime
from service.utilities.conversion import Conversions

class SettingsManager():

    
    # operational section & fields
    section_operational = 'Operational'
    field_rain_delay = 'rainDelay'
    field_city = 'city'
    field_country = 'country'
    field_kill_switch = 'kill_switch'

    # Logging section and fields
    section_logging = 'Logging'
    field_console_log_level = 'consoleLogLevel'
    field_database_log_level = 'databaseLogLevel'

    # Notify section and fields
    section_notifications = 'Notifications'
    field_notify_on_error = 'notifyOnError'
    field_notify_on_watering_start = 'notifyOnWateringStart'
    field_notify_on_watering_end = 'notifyOnWateringEnd'

    #Display section and fields
    section_display = 'Display'
    field_theme = 'theme'

    # Locks for each property so we don't read while a write is ongoing
    lockRainDelay = Lock()
    lockLoggingLevel = Lock()
    lockNotificationSettings = Lock()

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
    def setRainDelay(self, date):
        # self.readConfig()
        self.config[SettingsManager.section_operational][SettingsManager.field_rain_delay] = date
        self.save()

        datetimeFormat = None
        if date is not None and date is True:
            # Convert the string to a date and send via event mgr
            datetimeFormat = Conversions.convertRainDelaySettingToDatetime(date)
            
        shared_events.event_publisher.publishRainDelayUpdated(datetimeFormat)
    
    def getRainDelay(self):
        # self.readConfig()
        rainDelay = self.config[SettingsManager.section_operational][SettingsManager.field_rain_delay]

        if rainDelay == '':
            return None
            
        return(self.config[SettingsManager.section_operational][SettingsManager.field_rain_delay])

    def setCity(self, city):
        # self.readConfig()
        self.config[SettingsManager.section_operational][SettingsManager.field_city] = city
        self.save()
    
    def getCity(self):
        # self.readConfig()
        return(self.config[SettingsManager.section_operational][SettingsManager.field_city])

    def setCountry(self, country):
        # self.readConfig()
        self.config[SettingsManager.section_operational][SettingsManager.field_country] = country
        self.save()
    
    def getCountry(self):
        # self.readConfig()
        return(self.config[SettingsManager.section_operational][SettingsManager.field_country])
    
    def setKillSwitch(self, kill_switch):
        self.config[SettingsManager.section_operational][SettingsManager.field_kill_switch] = str(kill_switch)
        self.save()
        shared_events.event_publisher.publishKillSwitchUpdated()

    
    def getKillSwitch(self):
        # self.readConfig()
        return(self.config[SettingsManager.section_operational].getboolean(SettingsManager.field_kill_switch))

    ########################################
    #  Logging Fields
    ########################################
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


    ########################################
    #  Notification Fields
    ########################################
    
    def setNotifyOnError(self, value):
        self.config[SettingsManager.section_notifications][SettingsManager.field_notify_on_error] = str(value)
        self.save()
        shared_events.event_publisher.publishNotificationConfigUpdated()

    
    def getNotifyOnError(self):
        # self.readConfig()
        return(self.config[SettingsManager.section_notifications].getboolean(SettingsManager.field_notify_on_error))

    def setNotifyOnWateringStart(self, value):
        self.config[SettingsManager.section_notifications][SettingsManager.field_notify_on_watering_start] = str(value)
        self.save()
        shared_events.event_publisher.publishNotificationConfigUpdated()
    
    def getNotifyOnWateringStart(self):
        # self.readConfig()
        return(self.config[SettingsManager.section_notifications].getboolean(SettingsManager.field_notify_on_watering_start))

    def setNotifyOnWateringEnd(self, value):
        self.config[SettingsManager.section_notifications][SettingsManager.field_notify_on_watering_end] = str(value)
        self.save()
        shared_events.event_publisher.publishNotificationConfigUpdated()
    
    def getNotifyOnWateringEnd(self):
        # self.readConfig()
        return(self.config[SettingsManager.section_notifications].getboolean(SettingsManager.field_notify_on_watering_end))

    def setAllNotificationPreferences(self, start, end, error):
        self.config[SettingsManager.section_notifications][SettingsManager.field_notify_on_watering_start] = str(start)
        self.config[SettingsManager.section_notifications][SettingsManager.field_notify_on_watering_end] = str(end)
        self.config[SettingsManager.section_notifications][SettingsManager.field_notify_on_error] = str(error)
        self.save()
        shared_events.event_publisher.publishNotificationConfigUpdated()
    
    ##############
    # Display settings
    ##############
    def setTheme(self, theme):
        # self.readConfig()
        self.config[SettingsManager.section_display][SettingsManager.field_theme] = theme
        self.save()
    
    def getTheme(self):
        # self.readConfig()
        return(self.config[SettingsManager.section_display][SettingsManager.field_theme])


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



