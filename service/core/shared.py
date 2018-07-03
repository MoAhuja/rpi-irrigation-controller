# from service.core.event_publisher import EventPublisher
# from service.engine import Engine
from threading import Lock
# from service.system.settings_manager import SettingsManager
from service.utilities.logger import Logger

logger = Logger()

# Locks
lockNextRunSchedule = Lock()
lockActiveZones = Lock()



