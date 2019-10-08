isPIControllerEnabled = False
# from service.rest_mappers.relay_rest_mapper import RelayRestMapper
from service.database.relay_dbo import RelayDBO
from service.database.db_schema import RpiPinMapper
 

try:
    import RPi.GPIO as GPIO
    
    isPIControllerEnabled = True
except:
    print("Can't import GPIO, must not be a RPI. Going to disable PIController functionality.")
from service.core import shared

# This class manipulates the PINS on the raspberry pi
class PIController():
    isInitialized = False;
    def initializePINS(self):
        # Fetch all the required pins from the DB
        # TODO: Initialize all pin to BCD & Pull them down or whatever
        
        # Initialize all the pins to BCD

        if isPIControllerEnabled is True:

            if PIController.isInitialized is False:
                shared.logger.debug(self, "Initializing Pins")
                GPIO.setmode(GPIO.BCM)

                # Fetch all the relays
                rm = RelayDBO()
                relay_list = rm.retrieveRelays(asJSON = False)

                chan_list = []

                for pin_mapping in relay_list:
                    shared.logger.debug(self, "Initializing Pin: " + str(pin_mapping.rpi_pin))
                    chan_list.append(pin_mapping.rpi_pin)
                
                GPIO.setup(chan_list, GPIO.OUT, initial=GPIO.HIGH)

                PIController.isInitialized = True
            else:
                shared.logger.debug(self, "Already initialized pins, no need to re-init")

        #TODO: Add logic to support re-initialization of pins change
        
        # Set all the pins to their closed state/no electricity flowing (valve = off)
        # Loop through all the pins and set them as output pins
        #GPIO.setup(1, GPIO.OUT, initial=GPIO.LOW)

    def __init__(self):
        # TODO: Initialize all the pins
        self.initializePINS()
    
    def activatePIN(self, pin):
        #Add check to make sure PIN is numeric and one of the initialized pins
        shared.logger.debug(self,"Activating PIN:" + str(pin))

        if isPIControllerEnabled is True:
            GPIO.output(pin, GPIO.LOW)
        return True

    def deactivatePIN(self, pin):
        shared.logger.debug(self, "Deactivating PIN:" + str(pin))

        if isPIControllerEnabled is True:
            GPIO.output(pin, GPIO.HIGH)

        return True