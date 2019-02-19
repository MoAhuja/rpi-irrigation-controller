from service.rest_mappers.base_rest_mapper import BaseRestMapper
from service.database.db_schema import EnumLogLevel, Logs
from service.database.log_dbo import LogDBO


class LogsRestMapper(BaseRestMapper):

    ERROR_TYPE_INVALID_LOG_LEVEL = "Inavlid log level. Value must be one of [1 = ERROR, 2 = INFO, 3 = DEBUG]"
    def __init__(self):
        self.logDBO = LogDBO()

    
    def getAllLogs(self, page, page_size):
        allLogs = self.logDBO.retrieveAllLogs(page, page_size, asJSON=True)

        responseData = {}
        responseData["LOGS"] = allLogs

        return self.returnSuccessfulResponse(responseData)
    
    def getLogsByLevel(self, level, page, page_size):
        
        try:
            levelAsInt = int(level)
        except:
            self.raiseBadRequestException(Logs.FIELD_LEVEL, BaseRestMapper.ERROR_TYPE_INVALID_TYPE_MUST_BE_INT, None, None)
        
        # Check that it's in the range of 1-3
        if not levelAsInt in [EnumLogLevel.DEBUG.value, EnumLogLevel.INFO.value, EnumLogLevel.ERROR.value]:
            self.raiseBadRequestException(Logs.FIELD_LEVEL, LogsRestMapper.ERROR_TYPE_INVALID_LOG_LEVEL)

        allLogs = self.logDBO.retrieveAllLogsByLevel(levelAsInt, page, page_size, asJSON=True, )

        responseData = {}
        responseData["LOGS"] = allLogs

        return self.returnSuccessfulResponse(responseData)