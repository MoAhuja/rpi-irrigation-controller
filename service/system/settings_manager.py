import configparser
from service.utilities.logger import Logger
import os

class SettingsManager():

    
    operational = 'Operational'
    rain_delay = 'RainDelayInHours'

    def __init__(self):

        Logger.debug(self, "Initializing Settings Manager")

        # Create an instance of the config parser
        self.filePath = os.path.join(os.path.abspath(os.path.dirname(__file__)), '', 'settings.ini')
        self.config = configparser.ConfigParser()
        self.config.read(self.filePath)
    
    def setRainDelay(self, hours):
        self.config[SettingsManager.operational][SettingsManager.rain_delay] = str(hours)
        self.save()
    
    def getRainDelay(self):
        return(int(self.config[SettingsManager.operational][SettingsManager.rain_delay]))

    def save(self):
        with open(self.filePath, 'w') as settings_file:
            self.config.write(settings_file)



