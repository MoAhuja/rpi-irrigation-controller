from service.database.base_db_operations import BaseDBOperations
from service.utilities.logger import Logger
from service.core import shared_events, shared
 
from service.database.db_schema import Base,PushBulletUsers
 



class NotificationUsersDBO(BaseDBOperations):

    def __init__(self):
        # BaseDBOperations.__init__(self)
        self.event_pub = shared_events.event_publisher

    def addPushBulletUser(self, name, api_key):
        self.initialize()

        user =  PushBulletUsers(name=name, api_key=api_key)
   
        self.session.add(user)
        self.session.flush()
        self.session.commit()

    
    def deletePushBulletUser(self, name):
        self.initialize()

        self.session.query(PushBulletUsers).filter(PushBulletUsers.name == name).delete()
        self.session.commit()

    def getPushBulletUsers(self):

        self.initialize()
        users = self.session.query(PushBulletUsers).all()
        self.session.flush()

        userDict = []
        for user in users:
            userDict.append(user.toDictionary())
        
        return userDict
        
