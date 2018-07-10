
from threading import Lock
from service.utilities.logger import Logger

logger = Logger()

# Locks
lockNextRunSchedule = Lock()
lockActiveZones = Lock()



