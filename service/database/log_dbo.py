from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from service.database.base_db_operations import BaseDBOperations
from service.database.db_schema import Logs
# from service.utilities.logger import Logger

 
from service.database.db_schema import Base, Logs, EnumLogLevel
 
#Management variables
class LogDBO(BaseDBOperations):

    def logMessage(self, datetime, level, component, message):
        self.initialize()

        log =  Logs(datetime=datetime, level=level, component=component, message=message)
       
        # current_db_sessions = self.session.object_session(log)
        # current_db_sessions.add(log)
        # current_db_sessions.flush()
        # current_db_sessions.commit()
        self.session.add(log)
        self.session.flush()
        self.session.commit()

    #     #retrieve the zone_id
    def retrieveAllLogsByLevel(self, logLevel, asJSON=False):

        self.initialize()
        if logLevel == 1:
            enumLevel = EnumLogLevel.ERROR
        elif logLevel == 2:
            enumLevel = EnumLogLevel.INFO
        elif logLevel == 3:
            enumLevel = EnumLogLevel.DEBUG

        logEntries = self.session.query(Logs).filter_by(level=enumLevel).all()
        self.session.flush()

        if asJSON is True:
            logDict = []
            for log in logEntries:
                logDict.append(log.toDictionary())
            
            return logDict
        else:
            return logEntries
    
    
    
    def retrieveAllLogs(self, asJSON=False):
        self.initialize()
        logEntries = self.session.query(Logs).all()
        self.session.flush()

        if asJSON is True:
            logDict = []
            for log in logEntries:
                logDict.append(log.toDictionary())
            
            return logDict
        else:
            return logEntries
    
    # def retrieveLogsByRange(self, startRange, endRate):
    #     # 
  



