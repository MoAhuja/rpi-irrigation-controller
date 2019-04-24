from service.core import shared, shared_events
from service.notifications.pushbullet import PushBulletNotifier
from service.system.settings_manager import SettingsManager

class NotifierEngine():

    def __init__(self):
        self.notifyOnWateringStart = True
        self.notifyOnWateringEnd = True
        self.notifyOnError = False
        self.registeredNotifiers = set()
        self.settingsMgr = SettingsManager()

        # Register to listen for the watering start, stop and error events
        shared_events.event_publisher.register(self, listenForNotificationConfigChanges=True, listenForWateringStarted=True, listenForWateringStopped=True, listenForError=True)

        # load notification preferences
        self.loadNotificationPreferences()

       
    def loadRegisteredNotifiers():
        # self.registeredNotifiers.clear()

         # register all the notifiers
        self.registeredNotifiers.add(PushBulletNotifier())
    
    def eventNotificationConfigUpdated(self):
        shared.logger.debug(self, "NotifierEngine - Notification preferences changed. Going to reload.")
        
        self.loadNotificationPreferences()

    def loadNotificationPreferences(self):
        # Load what notifications to listen for (from settings)
        self.notifyOnWateringStart = self.settingsMgr.getNotifyOnWateringStart()
        self.notifyOnWateringEnd = self.settingsMgr.getNotifyOnWateringEnd()
        self.notifyOnError = self.settingsMgr.getNotifyOnError()


        shared.logger.debug(self, "Notification Preferences [start] " + str(self.notifyOnWateringStart))
        shared.logger.debug(self, "Notification Preferences [stop] " + str(self.notifyOnWateringEnd))
        shared.logger.debug(self, "Notification Preferences [error] " + str(self.notifyOnError))
        
    def eventWateringStarted(self, zone):
        if self.notifyOnWateringStart:
            self.sendMessageToAllNotifiers("Watering Started - '" + zone + "'")

    def eventWateringStopped(self, zone):
         if self.notifyOnWateringEnd:
            self.sendMessageToAllNotifiers("Watering Stopped - '" + zone + "'")

    def eventErrorRaised(self, error_message):
        if self.notifyOnError:
            self.sendMessageToAllNotifiers("ERROR: " + error_message)
    
    def sendMessageToAllNotifiers(self, message):
        for notifier in self.registeredNotifiers:
            notifier.sendMessageToAllSubscribers(message)
    

