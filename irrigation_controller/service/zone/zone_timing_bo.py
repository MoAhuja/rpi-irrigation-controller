class ZoneTiming():

   
    def __init__(self):
        self.zone = None
        self.start_time = None
        self.end_time = None

    @classmethod 
    def initialize(cls, zone, start_time, end_time):
        cl = cls()

        cl.zone = zone
        cl.start_time = start_time
        cl.end_time = end_time

        return cl

