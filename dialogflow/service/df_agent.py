from pydialogflow_fulfillment import DialogflowRequest
from pydialogflow_fulfillment import DialogflowResponse, SimpleResponse, OutputContexts
from service.agents.start_engine_agent import StartEngineAgent
import json
import pprint

class DialogFlowAgent():
    INTENT_GET_ZONE_INFO = "Get Zone Info by number"
    INTENT_START_ENGINE = "Start Engine"
    INTENT_STOP_ENGINE = "Stop Engine"



    def handleIntent(self, requestData):
        dialog_fulfillment = DialogflowRequest(requestData)
        
        pprint.pprint("===== Parameters ===== ")
        pprint.pprint(dialog_fulfillment.get_parameters())

        pprint.pprint("===== Output Contexts ===== ")
        outputContexts = dialog_fulfillment.get_ouputcontext_list()[0]
        pprint.pprint(outputContexts)
        pprint.pprint(outputContexts["parameters"])

        #Get the intent that was invoked
        intent = dialog_fulfillment.get_intent_displayName()
        
        #Depending on which intent was invoked, call the appropriate function to handle the payload
        if intent == self.INTENT_GET_ZONE_INFO:
            stringResponse =  self.getZoneInfoIntentHandler(dialog_fulfillment)
        elif intent == self.INTENT_START_ENGINE:
            stringResponse =  self.startEngineIntentHandler(dialog_fulfillment)
        else:
            stringResponse = "Request not supported"

        return self.generateSimpleResponse(dialog_fulfillment, stringResponse)

    def generateSimpleResponse(self, dialog_request, rawResponse):
        dialogflow_response = DialogflowResponse(rawResponse)

        dialogflow_response.add(SimpleResponse(rawResponse, rawResponse))
        dialogflow_response.add(OutputContexts(dialog_request.get_project_id(), dialog_request.get_session_id(), "Filters",200,{"Category": "Chicken"}))
        
        dialogflow_response
        return dialogflow_response


    def getZoneInfoIntentHandler(self, dialog_fulfillment):

        #Get the zone number
        dialog_fulfillment.get_parameter("zone_number")
        return self.lwAgent.getZoneInfo(6)
    
    def startEngineIntentHandler(self, dialog_fulfillment):
        print("StartEngineIntentHandler")
        response = StartEngineAgent().invoke()
        return response









