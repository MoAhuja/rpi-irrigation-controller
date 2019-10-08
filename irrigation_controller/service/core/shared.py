
from threading import RLock
from service.utilities.logger import Logger

logger = Logger()

# Locks
lockNextRunSchedule = RLock()
lockActiveZones = RLock()



