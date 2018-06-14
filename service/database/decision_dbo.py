
# from datetime import datetime
# from service.utilities.conversion import Conversions
from service.database.base_db_operations import BaseDBOperations
from service.utilities.logger import Logger
 
from service.database.db_schema import Zone, DecisionHistory

class DecisionDBO(BaseDBOperations):
    
    def insertDecisionEvent(self, decisionEvent):

        Logger.debug(self, "Inserting decision event")
        self.initialize()
        # self.session.add(decisionEvent)

        current_db_sessions = self.session.object_session(decisionEvent)
        current_db_sessions.add(decisionEvent)
        current_db_sessions.flush()
        current_db_sessions.commit()
    

