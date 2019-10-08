from pi.pi_controller import PIController
from pprint import pprint
from service.utilities.logger import Logger
from service.core import shared

class ZoneRPIController():

    def __init__(self):
        self.pi_controller = PIController()
    
    def activateZone(self, zone):

        if zone is not None:
            if zone.pin_config is None or zone.pin_config.rpi_pin is None:
                shared.logger.error(self, "RPI Pin not set for Zone " + zone.name + ". Unable to activate zone.")
                return False
            else:
                if self.pi_controller.activatePIN(zone.pin_config.rpi_pin):
                    shared.logger.info(self, "Zone " + zone.name + " activated (PIN: " + str(zone.pin_config.rpi_pin) + ")")
                    return True
        else:
            shared.logger.error(self, "Unable to activate zone. Zone object is null")
            return False
        
        return False

    def deactivateZone(self, zone):

        if zone is not None:
            if self.pi_controller.deactivatePIN(zone.pin_config.rpi_pin):
                shared.logger.info(self, "Zone " + zone.name + " deactivated (PIN: " + str(zone.pin_config.rpi_pin) + ")")
                return True
            
        else:
            shared.logger.error(self, "Unable to deactivate zone. Zone object is null") 
        
        return False
