import RPi.GPIO as GPIO

# This class manipulates the PINS on the raspberry pi
class PIController():

    def initializePINS(self):
        # Fetch all the required pins from the DB
        # TODO: Initialize all pin to BCD & Pull them down or whatever
        
        # Initialize all the pins to BCD
        GPIO.setmode(GPIO.BCM);


        
        chan_list = [23,4]    # add as many channels as you want!
                       # you can tuples instead i.e.:
                       #   chan_list = (11,12)
        GPIO.setup(chan_list, GPIO.OUT, initial=GPIO.HIGH)
        
        # Set all the pins to their closed state/no electricity flowing (valve = off)
        # Loop through all the pins and set them as output pins
        #GPIO.setup(1, GPIO.OUT, initial=GPIO.LOW)

    def __init__(self):
        # TODO: Initialize all the pins
        self.initializePINS()
    
    def activatePIN(self, pin):
        #Add check to make sure PIN is numeric and one of the initialized pins
        GPIO.output(pin, GPIO.LOW)
        return True

    def deactivatePIN(self, pin):
        GPIO.output(pin, GPIO.HIGH)
        return True