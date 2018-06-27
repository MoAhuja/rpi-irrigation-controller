from service.event_publisher import EventPublisher
# from service.engine import Engine
from threading import Lock


event_publisher = EventPublisher()
# engine = Engine()

# Locks
lockNextRunSchedule = Lock()
lockActiveZones = Lock()
