
# from datetime import datetime
# from service.utilities.conversion import Conversions
from service.database.base_db_operations import BaseDBOperations
from service.utilities.logger import Logger
from service.core import shared
from service.utilities.conversion import Conversions
 
from service.database.db_schema import Zone, DecisionHistory, EnumDecisionCodes

class DecisionDBO(BaseDBOperations):
    
    def insertDecisionEvent(self, decisionEvent):

        shared.logger.debug(self, "Inserting decision event")
        self.initialize()
        current_db_sessions = self.session.object_session(decisionEvent)
        current_db_sessions.add(decisionEvent)
        current_db_sessions.flush()
        current_db_sessions.commit()
        
    
    def fetchLastRunRecord(self, zone_id):

        shared.logger.debug(self, "Fetching last run record for " + str(zone_id))

        # Fetch by matching zone ID and decisionCode = deactivate
        self.initialize()

        lastRun = self.session.query(DecisionHistory).filter(DecisionHistory.zone_id==zone_id, DecisionHistory.decision==EnumDecisionCodes.DeactivateZone).order_by(DecisionHistory.event_time.desc()).limit(1).all()

        # lastRun = self.session.query(DecisionHistory).filter(DecisionHistory.zone_id==zone_id).limit(1).all()

        if lastRun is not None and len(lastRun) is not 0:
            return lastRun[0]

        return None
    
    def getAllDecisions(self, asJSON=False):
        self.initialize()
        decisionEntries = self.session.query(DecisionHistory).order_by(DecisionHistory.event_time.desc()).all()
        self.session.flush()

        if asJSON is True:
            dhDict = []
            for dh in decisionEntries:
                dhDict.append(dh.toDictionary())
            
            return dhDict
        else:
            return decisionEntries
    
    def getAllDecisionsForZone(self, zone_id, asJSON=False):
        self.initialize()
        decisionEntries = self.session.query(DecisionHistory).filter_by(zone_id=zone_id).order_by(DecisionHistory.event_time.desc()).all()
        self.session.flush()

        if asJSON is True:
            dhDict = []
            for dh in decisionEntries:
                dhDict.append(dh.toDictionary())
            
            return dhDict
        else:
            return decisionEntries

