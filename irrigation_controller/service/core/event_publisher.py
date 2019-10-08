# from service.utilities.logger import Logger

class EventPublisher():

    def __init__(self):
            self.zone_subscribers = set()
            self.rain_delay_subscribers = set()
            self.logging_subscribers = set()
            self.settings_subscribers = set()
            self.killswitch_subscribers = set()
            self.notification_config_subscribers = set()
            self.pushbullet_notification_users_updated_subscribers = set()
            self.watering_started_subscribers = set()
            self.watering_stopped_subscribers = set()
            self.error_subscribers = set()



    def register(self, who, listenForZoneUpdates=False, listenForRainDelayUpdates=False, listenForLoggingUpdates=False, listenForSettingsChanges=False, listenForKillSwitchUpdates=False, listenForNotificationConfigChanges=False, listenForPushBulletUserChanges = False, listenForWateringStarted=False, listenForWateringStopped=False, listenForError = False):
        if listenForZoneUpdates:
            self.zone_subscribers.add(who)
        
        if listenForRainDelayUpdates:
            self.rain_delay_subscribers.add(who)
        
        if listenForLoggingUpdates:
            self.logging_subscribers.add(who)
        
        if listenForSettingsChanges:
            self.settings_subscribers.add(who)
        
        if listenForKillSwitchUpdates:
            self.killswitch_subscribers.add(who)
        
        if listenForNotificationConfigChanges:
            self.notification_config_subscribers.add(who)

        if listenForWateringStarted:
            self.watering_started_subscribers.add(who)
        
        if listenForWateringStopped:
            self.watering_stopped_subscribers.add(who)
        
        if listenForError:
            self.error_subscribers.add(who)
        
        if listenForPushBulletUserChanges:
            self.pushbullet_notification_users_updated_subscribers.add(who)


    def unregister(self, who):
        self.rain_delay_subscribers.discard(who)
        self.zone_subscribers.discard(who)
        self.logging_subscribers.discard(who)
        self.settings_subscribers.discard(who)
        self.killswitch_subscribers.discard(who)
        self.notification_config_subscribers.discard(who)
        self.error_subscribers.discard(who)
        self.watering_started_subscribers.discard(who)
        self.watering_stopped_subscribers.discard(who)
        self.pushbullet_notification_users_updated_subscribers(who)

    def publishZoneInfoUpdated(self):
        for subscriber in self.zone_subscribers.copy():
            subscriber.eventZoneInfoUpdated()
    
    def publishRainDelayUpdated(self, rainDelayDate):
        for subscriber in self.rain_delay_subscribers.copy():
            subscriber.eventRainDelayUpdated(rainDelayDate)
    
    def publishLogLevelUpdated(self):
        for subscriber in self.logging_subscribers.copy():
            subscriber.eventLogLevelUpdated()
    
    def publishSettingsUpdated(self):
        for subscriber in self.settings_subscribers.copy():
            # print(subscriber)
            subscriber.eventSettingsUpdated()
    
    def publishKillSwitchUpdated(self):
        for subscriber in self.killswitch_subscribers.copy():
            subscriber.eventKillSwitchUpdated()
    
    def publishNotificationConfigUpdated(self):
        for subscriber in self.notification_config_subscribers.copy():
            subscriber.eventNotificationConfigUpdated()
    
    def publishPushbulletUserListUpdated(self):
        for subscriber in self.pushbullet_notification_users_updated_subscribers.copy():
            subscriber.eventNotificationPusbulletUsersUpdated()
    
    def publishWateringStarted(self, zone):
        for subscriber in self.watering_started_subscribers.copy():
            subscriber.eventWateringStarted(zone)
    
    def publishWateringStopped(self, zone):
        for subscriber in self.watering_stopped_subscribers.copy():
            subscriber.eventWateringStopped(zone)

    def publishError(self, errorMessage):
        for subscriber in self.error_subscribers.copy():
            subscriber.eventErrorRaised(errorMessage)

      
