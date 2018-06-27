from pi.pi_controller import PIController
from pprint import pprint
from service.utilities.logger import Logger

class ZoneRPIController():

    def __init__(self):
        self.pi_controller = PIController()
    
    def activateZone(self, zone):

        if zone is not None:
            if zone.pin_config is None or zone.pin_config.rpi_pin is None:
                Logger.error(self, "RPI Pin not set for Zone " + zone.name + ". Unable to activate zone.")
            else:
                self.pi_controller.activatePIN(zone.pin_config.rpi_pin)
                Logger.info(self, "Zone " + zone.name + " activated (PIN: " + str(zone.pin_config.rpi_pin) + ")")
        else:
            Logger.error(self, "Unable to activate zone. Zone object is null")

    def deactivateZone(self, zone):
        if zone is not None:
            self.pi_controller.deactivatePIN(zone.pin_config.rpi_pin)
            Logger.info(self, "Zone " + zone.name + " deactivated (PIN: " + str(zone.pin_config.rpi_pin) + ")")
        else:
            Logger.error(self, "Unable to deactivate zone. Zone object is null") 