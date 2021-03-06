# from flask.ext.api import status
from service.rest_mappers.InvalidUsage import InvalidUsage
from service.core import shared
import json


class BaseRestMapper():

    FIELD_SUCCESS = "success"
    FIELD_NAME = "name"
    FIELD_VALUE = "value"
    FIELD_ERROR_TYPE = "error_type"

    HTTP_ERROR_CODE_BAD_REQUEST = 400
    HTTP_ERROR_CODE_SERVER_ERROR = 500


    # ERROR TYPES
    ERROR_TYPE_INVALID_VALUE = "Invalid Value"
    ERROR_TYPE_MANDATORY = "Value cannot be empty"
    ERROR_TYPE_FIELD_MISSING = "Mandatory field is missing"
    ERROR_TYPE_INVALID_TYPE_MUST_BE_BOOL = "Invalid data type - Value must be a boolean (True/False) without any quotes"
    ERROR_TYPE_INVALID_TYPE_MUST_BE_INT = "Invalid data type - Value must be an int"
    ERROR_TYPE_INVALID_TYPE_MUST_BE_STRING = "Invalid data type - Value must be a string"

    
    # Response is a dictionary of fields
    def returnSuccessfulResponse(self, responseDict=None):
        if responseDict is None:
            responseDict = {}

        if BaseRestMapper.FIELD_SUCCESS not in responseDict:
            self.injectRequestSuccessValue(responseDict, True)
        
        return json.dumps(responseDict)
    
    def raiseBadRequestException(self, fieldName, error_message, payload=None, invalid_value=None):
        shared.logger.debug(self, "Return bad request: " + error_message + "[" + fieldName + "]")
        raise InvalidUsage(self.HTTP_ERROR_CODE_BAD_REQUEST, fieldName, error_message, payload, invalid_value )
        
    def raiseServerErrorException(self, error_message="Unknown Error"):
        shared.logger.debug(self, "Return server error")
        raise InvalidUsage(self.HTTP_ERROR_CODE_SERVER_ERROR, error_message=error_message)
       
    # Helper functions
    def injectRequestSuccessValue(self, responseData, result):
        responseData[BaseRestMapper.FIELD_SUCCESS] = result
        return responseData
    
    # Throws an exception if the data type is not a boolean
    def validateMandatory(self, dataToValidate, field_name, json_data=None):
        if dataToValidate is None:
            self.raiseBadRequestException(field_name, BaseRestMapper.ERROR_TYPE_MANDATORY, json_data)
        elif type(dataToValidate) is str and len(dataToValidate) is 0:
            self.raiseBadRequestException(field_name, BaseRestMapper.ERROR_TYPE_MANDATORY, json_data)

    
    # Throws an exception if the data type is not a boolean
    def validateIsProvidedAndBool(self, dataToValidate, field_name, json_data=None):
        self.validateMandatory(dataToValidate, field_name, json_data)

        if type(dataToValidate) is not bool:
            self.raiseBadRequestException(field_name, BaseRestMapper.ERROR_TYPE_INVALID_TYPE_MUST_BE_BOOL, json_data, dataToValidate)
    
    # Throws an exception if the data type is not an integer
    def validateIsProvidedAndInt(self, dataToValidate, field_name, json_data=None):
        self.validateMandatory(dataToValidate, field_name, json_data)
        
        if type(dataToValidate) is not int:
            # Try to parse it to an int
            try:
                parsedInt = int(dataToValidate)
                return parsedInt
            except:
                self.raiseBadRequestException(field_name, BaseRestMapper.ERROR_TYPE_INVALID_TYPE_MUST_BE_INT, json_data, dataToValidate)

        else:
            return dataToValidate
    
    def validateIsInt(self, dataToValidate, field_name, json_data=None):
        if dataToValidate is not None:
            if type(dataToValidate) is not int:
                shared.logger.debug(self, "validateIsInt: It is not an int. Going to cast.")
                # Try to parse it to an int
                try:
                    parsedInt = int(dataToValidate)
                    shared.logger.debug(self, "Parsed the int")
                
                    return parsedInt
                except:
                    self.raiseBadRequestException(field_name, BaseRestMapper.ERROR_TYPE_INVALID_TYPE_MUST_BE_INT, json_data, dataToValidate)

            else:
                shared.logger.debug(self, "Already an int")
                
                return dataToValidate
        else:
            return dataToValidate
        
    # Throws an exception if the data type is not a string
    def validateIsProvidedAndString(self, dataToValidate, field_name, json_data=None):
        self.validateMandatory(dataToValidate, field_name, json_data)
        
        if type(dataToValidate) is not str:
            self.raiseBadRequestException(field_name, BaseRestMapper.ERROR_TYPE_INVALID_TYPE_MUST_BE_STRING, json_data, dataToValidate)
    
    def getKeyOrThrowException(self, dictionary, key, json_data):
        data = None
        try:
            shared.logger.debug(self, "Fetching " + key + " from dict")
            data = dictionary[key]
        except KeyError:
            self.raiseBadRequestException(key, self.ERROR_TYPE_FIELD_MISSING,json_data)
        
        return data

    def getKeyOrSetAsNone(self, dictionary, key):
        data = None
        try:
            data = dictionary[key]
        except KeyError:
            return None
        
        return data

    

