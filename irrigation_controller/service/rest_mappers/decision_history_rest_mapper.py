from service.rest_mappers.base_rest_mapper import BaseRestMapper
from service.database.decision_dbo import DecisionDBO
from service.zone.zone_data_manager import ZoneDataManager

class DecisionHistoryRestMapper(BaseRestMapper):

    ERROR_TYPE_NOT_A_VALID_ZONE = "Zone does not exist"
    def __init__(self):
        self.decisionDBO = DecisionDBO()
        self.zdm = ZoneDataManager()
    
    def getHistoryByZone(self, zone_id):

        try:
            zoneAsInt = int(zone_id)
        except:
            self.raiseBadRequestException("Zone ID", BaseRestMapper.ERROR_TYPE_INVALID_TYPE_MUST_BE_INT, None, None)
        
        # Check that the zone exists
        if self.zdm.retrieveZone(zoneAsInt) is None:
            self.raiseBadRequestException("Zone ID", DecisionHistoryRestMapper.ERROR_TYPE_NOT_A_VALID_ZONE, None)
        
        decisions = self.decisionDBO.getAllDecisionsForZone(zoneAsInt, asJSON=True)

        responseData = {}
        responseData["DecisionHistory"] = decisions

        return self.returnSuccessfulResponse(responseData)
    
    def getHistoryForAllZones(self):
        decisions = self.decisionDBO.getAllDecisions(asJSON=True)

        responseData = {}
        responseData["DecisionHistory"] = decisions

        return self.returnSuccessfulResponse(responseData)


