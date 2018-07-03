# from flask.ext.api import status
from service.rest_mappers.InvalidUsage import InvalidUsage

import json

class BaseRestMapper():

    FIELD_SUCCESS = "success"
    FIELD_NAME = "name"
    FIELD_VALUE = "value"
    FIELD_ERROR_TYPE = "error_type"

    HTTP_ERROR_CODE_BAD_REQUEST = 400


    # ERROR TYPES
    ERROR_TYPE_INVALID_VALUE = "Invalid Value"

    
    # Response is a dictionary of fields
    def returnSuccessfulResponse(self, responseDict=None):
        if responseDict is None:
            responseDict = {}

        if BaseRestMapper.FIELD_SUCCESS not in responseDict:
            self.injectRequestSuccessValue(responseDict, True)
            
        return json.dumps(responseDict)
    
    def returnBadRequest(self, fieldName, error_type, payload=None):
        raise InvalidUsage(self.HTTP_ERROR_CODE_BAD_REQUEST, fieldName, error_type, payload )
        

    # Helper functions
    def injectRequestSuccessValue(self, responseData, result):
        responseData[BaseRestMapper.FIELD_SUCCESS] = result
        return responseData
