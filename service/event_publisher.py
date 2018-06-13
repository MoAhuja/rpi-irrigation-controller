from service.utilities.logger import Logger

class EventPublisher():

    def __init__(self):
            self.subscribers = set()

    def register(self, who):
        self.subscribers.add(who)

    def unregister(self, who):
        self.subscribers.discard(who)

    def publishZoneInfoUpdated(self):
        Logger.info(self, "Zone info updated. Publishing event to subscribers")
        for subscriber in self.subscribers:
            subscriber.publishZoneInfoUpdated()