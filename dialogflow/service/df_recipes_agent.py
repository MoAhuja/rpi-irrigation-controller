from pydialogflow_fulfillment import DialogflowRequest
from pydialogflow_fulfillment import DialogflowResponse, SimpleResponse, OutputContexts
from flask import Flask, jsonify, Response
from service.agents.start_engine_agent import StartEngineAgent
import json
import pprint
import os
import codecs

class DialogFlowRecipesAgent():
    INTENT_GET_RECIPES = "Get Recipes"
    INTENT_SELECT_RECIPE = "Select Recipe"
    INTENT_STOP_ENGINE = "Stop Engine"



    def handleIntent(self, requestData):
        dialog_fulfillment = DialogflowRequest(requestData)
        
        # pprint.pprint("===== Parameters ===== ")
        # pprint.pprint(dialog_fulfillment.get_parameters())

        # pprint.pprint("===== Output Contexts ===== ")
        # outputContexts = dialog_fulfillment.get_ouputcontext_list()[0]
        # pprint.pprint(outputContexts)
        # pprint.pprint(outputContexts["parameters"])

        #Get the intent that was invoked
        intent = dialog_fulfillment.get_intent_displayName()
        
        #Depending on which intent was invoked, call the appropriate function to handle the payload
        if intent == self.INTENT_GET_RECIPES:
            return  self.getRecipesIntentHandler(dialog_fulfillment)
        elif intent == self.INTENT_SELECT_RECIPE:
            return self.selectRecipesIntentHandler(dialog_fulfillment)
        else:
            return self.generateSimpleResponse(dialog_fulfillment, "Request not supported")

         

    def generateSimpleResponse(self, dialog_request, rawResponse):
        dialogflow_response = DialogflowResponse(rawResponse)

        dialogflow_response.add(SimpleResponse(rawResponse, rawResponse))
        dialogflow_response.add(OutputContexts(dialog_request.get_project_id(), dialog_request.get_session_id(), "Filters",200,{"Category": "Chicken"}))
        
        dialogflow_response
        return dialogflow_response


    def getRecipesIntentHandler(self, dialog_fulfillment):

        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        rel_path = "file_responses/food_list.json"
        
        abs_file_path = os.path.join(script_dir, rel_path)
        pprint.pprint(abs_file_path)
        with open(abs_file_path, 'r') as f:
            data = json.load(f)
            pprint.pprint(json.dumps(data))
            
            resp = Response(json.dumps(data), mimetype='application/json')
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp

    def selectRecipesIntentHandler(self, dialog_fulfillment):

        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        rel_path = "file_responses/select_recipe.html"
        
        abs_file_path = os.path.join(script_dir, rel_path)
        pprint.pprint(abs_file_path)
        with codecs.open(abs_file_path, 'r') as f:
            data = f.read()
            pprint.pprint(data)
            resp = Response(data, mimetype='text/html')
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp










