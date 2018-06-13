class ActiveZone():

   
    def __init__(self):
        self.zone = None
        self.shutoff_time = None

    @classmethod 
    def initialize(cls, zone, shutoff_time):
        cl = cls()

        cl.zone = zone
        cl. shutoff_time = shutoff_time

        return cl

