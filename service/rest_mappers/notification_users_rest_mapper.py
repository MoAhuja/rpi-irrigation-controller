from service.rest_mappers.base_rest_mapper import BaseRestMapper
from service.database.db_schema import EnumLogLevel, Logs
from service.database.notifications_users_dbo import NotificationUsersDBO
from service.core import shared
import json

class NotificationUsersRestMapper(BaseRestMapper):

    FIELD_NAME = "name"
    FIELD_API_KEY = "api_key"

    def __init__(self):
        self.notificationUsersDBO = NotificationUsersDBO()

    
    def getPushBulletNotificationUsers(self):
        users = self.notificationUsersDBO.getPushBulletUsers()

        responseData = {}
        responseData["users"] = users

        return self.returnSuccessfulResponse(responseData)

    def deletePushBulletNotificationUser(self, name):

        self.notificationUsersDBO.deletePushBulletUser(name)

        return self.returnSuccessfulResponse()
    
    def addPushBulletUser(self, json_data):
        
        shared.logger.debug(self, "addPushBulletUser - Entered")
        shared.logger.debug(self, "Data = " + json.dumps(json_data))
        
        name = self.getKeyOrThrowException(json_data, NotificationUsersRestMapper.FIELD_NAME, json_data)
        api_key = self.getKeyOrThrowException(json_data, NotificationUsersRestMapper.FIELD_API_KEY, json_data)
        
        

        # Validate values are bools
        self.validateIsProvidedAndString(name,  NotificationUsersRestMapper.FIELD_NAME, json_data)
        self.validateIsProvidedAndString(api_key, NotificationUsersRestMapper.FIELD_API_KEY, json_data)
        
        response = self.notificationUsersDBO.addPushBulletUser(name, api_key)
        return self.returnSuccessfulResponse()