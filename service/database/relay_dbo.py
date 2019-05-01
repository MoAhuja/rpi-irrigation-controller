from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from service.database.base_db_operations import BaseDBOperations
from service.database.db_schema import RpiPinMapper
import queue
import threading
# from service.utilities.logger import Logger

 
from service.database.db_schema import Base, Logs, EnumLogLevel
 
#Management variables
class RelayDBO(BaseDBOperations):

    def assignRelayToPin(self, relay, pin):
        
        self.initialize()

        mapping =  RpiPinMapper(relay_id = relay, rpi_pin = pin)
        self.session.add(mapping)
        self.session.flush()
        self.session.commit()
        # self.queue.put(log)

    def retrieveByPin(self, pin, asJSON=False):

        self.initialize()

        mapping = self.session.query(RpiPinMapper).filter_by(rpi_pin=pin)
        self.session.flush()

        if (mapping.count() > 0):
            if asJSON is True:
                return mapping[0].toDictionary()
            else:
                return mapping
        else:
            return None
    
    def retrieveRelays(self, asJSON):
        self.initialize()
        relays = self.session.query(RpiPinMapper).all()
        self.session.flush()

        if asJSON is True:
            jsonDict =  []
            for relay in relays:
                jsonDict.append(relay.toDictionary())
            return jsonDict   
        else:         
            return relays

        

    def retrieveByRelay(self, relay, asJSON=False):

       
        self.initialize()

        mapping = self.session.query(RpiPinMapper).filter_by(relay_id=relay)
        self.session.flush()

        if(mapping.count() > 0):
            if asJSON is True:
                return mapping[0].toDictionary()
            else:
                return mapping
        else:
            return None
    
    def deleteRelayMapping(self, relay):

        self.initialize()

        self.session.query(RpiPinMapper).filter(RpiPinMapper.relay_id == relay).delete()
        self.session.commit()
    
    def doesRelayMappingExist(self, relay):

        result = self.retrieveByRelay(relay, True)

        if (result is None):
            return False
        else:
            return  (len(result) > 0)

    def doesPinMappingExist(self, pin):

        result = self.retrieveByPin(pin, True)

        if (result is None):
            return False
        else:
            return  (len(result) > 0)



        
  



