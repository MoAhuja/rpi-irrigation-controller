from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from service.database.base_db_operations import BaseDBOperations
# from service.utilities.logger import Logger

 
from service.database.db_schema import Base, Logs, EnumLogLevel
 
#Management variables
class LogDBO(BaseDBOperations):

    def logMessage(self, level, component, message):
        self.initialize()

        log =  Logs(level=level, component=component, message=message)
       
        # current_db_sessions = self.session.object_session(log)
        # current_db_sessions.add(log)
        # current_db_sessions.flush()
        # current_db_sessions.commit()
        self.session.add(log)
        self.session.flush()
        self.session.commit()

    #     #retrieve the zone_id
    def retrieveAllLogsByLevel(logLevel):

        self.initialize()
        logEntries = self.session.query(Logs).filter(level=logLevel).all()
        self.session.flush()
        return logEntries
  



