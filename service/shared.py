from service.event_publisher import EventPublisher
# from service.engine import Engine
from threading import Lock
from service.system.settings_manager import SettingsManager


event_publisher = EventPublisher()
settingsManager = SettingsManager()
# engine = Engine()

# Locks
lockNextRunSchedule = Lock()
lockActiveZones = Lock()
