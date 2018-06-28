from service.utilities.logger import Logger

class EventPublisher():

    def __init__(self):
            self.zone_subscribers = set()
            self.rain_delay_subscribers = set()

    def register(self, who, listenForZoneUpdates, listenForRainDelayUpdates):
        if listenForZoneUpdates:
            self.zone_subscribers.add(who)
        
        if listenForRainDelayUpdates:
            self.rain_delay_subscribers.add(who)

    def unregister(self, who):
        self.rain_delay_subscribers.discard(who)
        self.zone_subscribers.discard(who)

    def publishZoneInfoUpdated(self):
        Logger.info(self, "Zone info updated. Publishing event to subscribers")
        for subscriber in self.zone_subscribers:
            subscriber.eventZoneInfoUpdated()
    
    def publishRainDelayUpdated(self):
        Logger.info(self, "Rain delay updated. Publishing event to subscribers")
        for subscriber in self.rain_delay_subscribers:
            subscriber.eventRainDelayUpdated()
