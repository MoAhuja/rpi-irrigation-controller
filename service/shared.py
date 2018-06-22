
from service.event_publisher import EventPublisher
from service.engine import Engine


event_publisher = EventPublisher()
engine = Engine(event_publisher)

