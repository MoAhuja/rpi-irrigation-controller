from pydialogflow_fulfillment import DialogflowRequest
from pydialogflow_fulfillment import DialogflowResponse, SimpleResponse
from service.lw_agent import LawnWatcherAgent
import pprint

class DialogFlowAgent():
    INTENT_GET_ZONE_INFO = "Get Zone Info by number"


    def __init__(self):
        self.lwAgent = LawnWatcherAgent()

    def handleIntent(self, requestData):
        print("test1")
        dialog_fulfillment = DialogflowRequest(requestData)

        intent = dialog_fulfillment.get_intent_displayName()

        if intent == self.INTENT_GET_ZONE_INFO:
            stringResponse =  self.getZoneInfo((dialog_fulfillment))


        return self.generateSimpleResponse(stringResponse)

    def generateSimpleResponse(self, rawResponse):
        dialogflow_response = DialogflowResponse(rawResponse)
        dialogflow_response.add(SimpleResponse(rawResponse, rawResponse))
        return dialogflow_response


    def getZoneInfo(self, dialog_fulfillment):

        #Get the zone number
        dialog_fulfillment.get_paramter("zone_number")

        return self.lwAgent.getZoneInfo(6)





