
from service.rest_mappers.base_rest_mapper import BaseRestMapper
from service.database.relay_dbo import RelayDBO
import json
from flask import jsonify
from service.utilities.conversion import Conversions
from service.database.db_schema import RpiPinMapper
from service.core import shared
import sys

class RelayRestMapper(BaseRestMapper):

    # FIELD_RELAY = "relay"
    # FIELD_PIN = "pin"

    # Logic errors
    ERROR_TYPE_PIN_ALREADY_ASSIGNED = "Invalid config - Pin already mapped to another relay"
    ERROR_TYPE_RELAY_ALREADY_ASSIGNED = "Invalid config - Relay already mapped to another pin"
    ERROR_TYPE_PIN_NOT_NUMERIC = "Invalid Value - PIN must be numeric"
    ERROR_TYPE_RELAY_NOT_NUMERIC = "Invalid Value - Relay must be numeric"
    ERROR_TYPE_INVALID_DAY_TYPE = "Invalid Value - Days must range between 0 and 6"
    # ERROR_TYPE_ZONE_NAME_MUST_BE_UNIQUE = "Zone name already exists"
    # ERROR_TYPE_ZONE_ID_NOT_FOUND = "Zone ID not found"
    

    def __init__(self):
        self.rm = RelayDBO()

    
    def createRelayToPinMapping(self, json_data):
        
        shared.logger.debug(self, "createRelayToPinMapping -> Data = " + json.dumps(json_data))

        relay = self.getKeyOrThrowException(json_data, RpiPinMapper.FIELD_RELAY, json_data)
        pin = self.getKeyOrThrowException(json_data, RpiPinMapper.FIELD_PIN, json_data)
        

        relay = self.validateIsProvidedAndInt(relay, RpiPinMapper.FIELD_RELAY, json_data)
        pin = self.validateIsProvidedAndInt(pin, RpiPinMapper.FIELD_PIN, json_data)

        # Validate the relay doesn't exist
        if(self.rm.doesRelayMappingExist(relay)):
            self.raiseBadRequestException(RpiPinMapper.FIELD_RELAY, RelayRestMapper.ERROR_TYPE_RELAY_ALREADY_ASSIGNED)
 
        # Validate the pin doesn't already exist
        if(self.rm.doesPinMappingExist(pin)):
            self.raiseBadRequestException(RpiPinMapper.FIELD_PIN, RelayRestMapper.ERROR_TYPE_PIN_ALREADY_ASSIGNED)

        # Validate the pin doesn't already exist
        response = self.rm.assignRelayToPin(relay, pin)

        return self.returnSuccessfulResponse()
    
    def getRelays(self):

        response = {}
        response["relays"] = self.rm.retrieveRelays(True)
        return self.returnSuccessfulResponse(response)

    