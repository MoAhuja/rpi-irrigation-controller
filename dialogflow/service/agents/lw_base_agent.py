import requests
import json
import pprint

class LawnWatcherBaseAgent():
    GENERIC_ERROR_MESSAGE = "Something went wrong!"
    GENERIC_SUCCESS_MESSAGE = "Done!"
    URL = ""
    API_ENDPOINT = ""
    method = 0

    def __init__(self):
        
        self.URL = "http://localhost:5000"
        self.API_ENDPOINT = ""
        self.method = 0

    def getHeaders(self):
        headers = {'Content-Type': 'application/json', 'Authorization': 'Basic bW86dGVzdA=='}

        return headers


    #Override this in teh child class to handle the response data accordingly
    def handleResponse(self, responseData=None):
        return GENERIC_SUCCESS_MESSAGE
    
    def sendAndProcessRequest(self, payload=None):

        fullURL = self.URL +  self.API_ENDPOINT

        pprint.pprint(fullURL)
        pprint.pprint(payload)
        if self.method == 0:
            response = requests.get(fullURL, headers=self.getHeaders())
        elif self.method == 1:
            response = request.post(fullURL, headers=self.getHeaders(), json=payload)

        #Generic error handling
        if response.status_code == 200:
            return self.handleResponse(response.content)
        else:
            return self.GENERIC_ERROR_MESSAGE


    #def createUnAuthorizedResponse(self):
    #def createGenericFailureResponse(self):

