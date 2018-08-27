from service.database.notifications_users_dbo import NotificationUsersDBO
import requests
import json
from service.core import shared

class PushBulletNotifier():
    def __init__(self):
        self.api_keys = []
        self.dbo = NotificationUsersDBO()
        self.loadRegisteredSubscribers()

        
    
    def loadRegisteredSubscribers(self):
        shared.logger.debug(self, "PushBullet -  Loading subscribers")
        pbUsers = self.dbo.getPushBulletUsers()

        for user in pbUsers:
            self.api_keys.append(user["api_key"])
            shared.logger.debug(self, user["api_key"])

    def sendMessageToAllSubscribers(self, message):

        shared.logger.debug(self, "PushBullet - Sending Message [ " + message + "] to Subscribers")

        for key in self.api_keys:
            self.sendNotificationService(key, message)
            shared.logger.debug(self, "Sending message to: " + key)

        # Send message to each one
    
    def sendNotificationService(self, apikey, message):
       
        data_send = {"type": "note", "title": "Lawn Watcher", "body": message}
        requests.post(
            'https://api.pushbullet.com/v2/pushes',
            data=json.dumps(data_send),
            headers={'Authorization': 'Bearer ' + apikey,
                        'Content-Type': 'application/json'})
        
    
    # listen for API key change events and update the list
