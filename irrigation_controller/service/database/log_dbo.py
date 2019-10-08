from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from service.database.base_db_operations import BaseDBOperations
from service.database.db_schema import Logs
import queue
import threading
# from service.utilities.logger import Logger

 
from service.database.db_schema import Base, Logs, EnumLogLevel
 
#Management variables
class LogDBO(BaseDBOperations):

    def __init__(self):
        self.queue = queue.Queue()
        self.heartbeat()


    def logMessage(self, datetime, level, component, message):
        
        log =  Logs(datetime=datetime, level=level, component=component, message=message)
       
        # current_db_sessions = self.session.object_session(log)
        # current_db_sessions.add(log)
        # current_db_sessions.flush()
        # current_db_sessions.commit()
        # self.session.add(log)
        # self.session.flush()
        # self.session.commit()
        self.queue.put(log)

    #     #retrieve the zone_id
    def retrieveAllLogsByLevel(self, logLevel,  page, page_size, asJSON=False):

       
        self.initialize()

        if logLevel == 1:
            enumLevel = EnumLogLevel.ERROR
        elif logLevel == 2:
            enumLevel = EnumLogLevel.INFO
        elif logLevel == 3:
            enumLevel = EnumLogLevel.DEBUG

        
        
        # Add the limit if the page size is greater than 0
        logEntries = []

        if(page_size > 0) and (page > 0):
            print("limiting logs by page and chunk")
            logEntries = self.session.query(Logs).filter_by(level=enumLevel).order_by(Logs.datetime.desc()).offset(page*page_size).limit(page_size)
        else:
            logEntries = self.session.query(Logs).filter_by(level=enumLevel).order_by(Logs.datetime.desc())

        self.session.flush()

        if asJSON is True:
            logList = []
            logDict = {}
            for log in logEntries:
                logList.append(log.toDictionary())
                   
            logDict["LOGS"] = logList
            if (page_size > 0) and (logEntries.count() < page_size):
                logDict["has_more"] = False
            else:
                logDict["has_more"] = True
            return logDict
        else:
            return logEntries
    
    
    
    def retrieveAllLogs(self, page, page_size, asJSON=False):
        self.initialize()

         # Add the limit if the page size is greater than 0
        logEntries = []

        if(page_size > 0) and (page > 0):
            print("limiting logs by page and chunk")
            logEntries = self.session.query(Logs).order_by(Logs.datetime.desc()).offset(page*page_size).limit(page_size)
        else:
            logEntries = self.session.query(Logs).order_by(Logs.datetime.desc())

        self.session.flush()

        if asJSON is True:
            logList = []
            logDict = {}
            for log in logEntries:
                logList.append(log.toDictionary())
                   
            logDict["LOGS"] = logList
            if (page_size > 0) and (logEntries.count() < page_size):
                logDict["has_more"] = False
            else:
                logDict["has_more"] = True
            return logDict
        else:
            return logEntries
    
    # def retrieveLogsByRange(self, startRange, endRate):
    #     # 
    def heartbeat(self):

        self.initialize()

       
        data = []
        # Grab all items from the queue
        while self.queue.empty() is False:
            data.append(self.queue.get())
        
        for log in data:
            self.session.add(log)
        

        self.session.flush()
        self.session.commit()


        threading.Timer(5, self.heartbeat).start()



        
  



