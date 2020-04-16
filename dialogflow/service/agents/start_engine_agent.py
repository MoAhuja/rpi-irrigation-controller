import pprint

from service.agents.lw_base_agent import LawnWatcherBaseAgent

class StartEngineAgent(LawnWatcherBaseAgent):
    
    START_ENGINE_SUCCESS_MESSAGE = "Engine started"


    def __init__(self):
        LawnWatcherBaseAgent.__init__(self)
        self.API_ENDPOINT = "/service_hub/engine/start"
        self.method = 0
    

    def invoke(self):
        message =  self.sendAndProcessRequest()
        pprint.pprint("Message is: " + message)

        return message

    def handleResponse(self, responseData=None):
        return self.START_ENGINE_SUCCESS_MESSAGE


