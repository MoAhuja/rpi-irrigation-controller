
# This class manipulates the PINS on the raspberry pi
class PIController():

    def initializePINS(self):
        # Fetch all the required pins from the DB
        # TODO: Initialize all pin to BCD & Pull them down or whatever
        a=0
        # Initialize all the pins to BCD
        # Set all the pins to their closed state/no electricity flowing (valve = off)

    def __init__(self):
        # TODO: Initialize all the pins
        self.initializePINS()
    
    def activatePIN(self, pin):
        return True

    def deactivatePIN(self, pin):
        return True