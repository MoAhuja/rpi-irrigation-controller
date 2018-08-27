from service.weather_hub.weather_center import WeatherCenter
from service.utilities.conversion import Conversions
from service.zone.zone_timing_bo import ZoneTiming
from service.database.decision_dbo import DecisionDBO
from service.core.scheduler import Scheduler
from service.zone.zone_controller import ZoneController
from service.core import shared
from service.system.settings_manager import SettingsManager
from service.notifications.notifier_engine import NotifierEngine

# Not sure i should be accessing DAO's at this layer, but it seems unneccessary to create a new object to track the same data
from service.database.db_schema import DecisionHistory, EnumDecisionCodes, EnumReasonCodes

# from pprint import pprint
from datetime import datetime
from service.utilities.logger import Logger
import threading

class Engine():

    decisionHistoryDBO = None
    weather_centre = None
    weather_profile = None
    evaluatingZones = False
    activeZones = []
    

    def __init__(self):
        
        self.scheduler = Scheduler()
        self.decisionHistoryDBO = DecisionDBO()
        self.zone_controller = ZoneController()
        self.weather_centre = WeatherCenter()
        self.settingsManager = SettingsManager()
        NotifierEngine()
        self.heartbeat()
        

    def checkAndDeactivateZones(self):
        # TODO: Determine if deactivation should be done if kill switch is on
        deactivateList = []

        # Loop through the activeZones list and check if the end time has been past
        shared.logger.debug(self,"Checking if any zones need to be deactivated")
        currentTime = datetime.now()

        # Lock because we don't want the active zones to change while we are iterating over them
        shared.logger.debug(self, "CheckAndDeactivateZones - Waiting to acquire lock: lockActiveZones")
        shared.lockActiveZones.acquire()

        try:

            for key, activeZone in self.zone_controller.activeZones.items():
                
                shared.logger.debug(self,"Deactivation Check: [Zone ID] = " + str(key) + ", [CurrentTime] = " + Conversions.convertDBTimeToHumanReadableTime(currentTime)+ ", [Deactivation Time] =  " + Conversions.convertDBTimeToHumanReadableTime(activeZone.end_time))
                if currentTime > activeZone.end_time:
                    
                    shared.logger.debug(self, "Adding zone to list pending deactivation")

                    # Add to list so we can remove it from our list of active zones
                    deactivateList.append(key)

        finally:
            shared.logger.debug(self, "CheckAndDeactivateZones - Releasing lock: lockActiveZones")
            shared.lockActiveZones.release()


        self.zone_controller.deactivateListOfZones(deactivateList, decisionHistoryReasonCode=EnumReasonCodes.AllConditionsPassed)
        shared.logger.debug(self,"Deactivation check complete")
        
        
        

    def checkAndActivateZones(self):
        
        if self.settingsManager.getKillSwitch() is True:
            shared.logger.info(self, "Kill Switch Enabled - Not going to perform zone schedule evaluation")
            return

        shared.logger.debug(self,"Evaluating Zones == " + str(self.evaluatingZones))

        # We need to make sure no one else is looping through the zones in case this gets invoked on another thread
        if self.evaluatingZones is False:

            shared.logger.debug(self,"Evaluating zones")
            # Set a flag indicating the zones are being evaluated
            self.evaluatingZones = True

            # Load the zones that we need to monitor
            self.scheduler.loadNextRunSchedule()

            shared.logger.debug(self,"Finished loading zones")

            # Get Time
            currentDateTime = datetime.now()
            currentTime = currentDateTime.time()
            shared.logger.debug(self, "Current Time is: " + Conversions.convertDBTimeToHumanReadableTime(currentTime))
            currentTemp = self.getCurrentTemp()
            shared.logger.debug(self, "Current Temperature is: " + str(currentTemp))
            
            
            rebuildSchedule = False

            shared.logger.debug(self, "CheckAndActivateZones - Waiting for lock: nextRunSchedule")
            shared.lockNextRunSchedule.acquire()
            try:
                for id, zonetiming in Scheduler.nextRunSchedule.items():
                    
                    shared.logger.debug(self, "Evaluating Zone: " + zonetiming.zone.name)

                    # Check if this zone is already active
                    # TODO: What do we do if two schedules overlap? I suppose they can't? Need to make sure of this.
                    # TODO: If they can't overlap, then we likely don't need this.
                    if id in self.activeZones:
                        shared.logger.debug(self,"Zone already active. Skipping evaluation.")
                        break

                    # Reset all the conditions
                    rainRuleMet = False
                    tempRuleMet = False
                
                    shared.logger.debug(self, "Activate if: " + str(zonetiming.start_time) + " < " + str(currentDateTime)  + " < " + str(zonetiming.end_time))
                    # Check if the current time is past the start time, but before the end time
                    if zonetiming.start_time <= currentDateTime < zonetiming.end_time:
                        rebuildSchedule = True

                        # Create a decision event w/ current info
                        decisionEvent = None
                        decisionEvent = DecisionHistory(zone=zonetiming.zone, event_time=currentDateTime, start_time=zonetiming.start_time, end_time=zonetiming.end_time)
                        # decisionEvent = DecisionHistory()
                        shared.logger.debug(self, "Current Time within boundries")
                        
                        #Check conditions
                        tempRuleMet = self.meetsTemperatureConditions(zonetiming.zone.temperature_rule, decisionEvent)
                        rainRuleMet = self.meetsRainConditions(zonetiming.zone.rain_rule, decisionEvent)
                        
                        activateZone = tempRuleMet * rainRuleMet
                        
                        if activateZone:
                            # Copy the zone timing object to the active running zones
                            self.zone_controller.activateZone(zonetiming, decisionEvent, EnumReasonCodes.AllConditionsPassed)
                        else:

                            #Log an event, if one is available to be logged.
                            self.decisionHistoryDBO.insertDecisionEvent(decisionEvent)
                            self.decisionHistoryDBO.saveAndClose()

                        # Since the current time can only fall in one schedule, we can stop evaluating
                        # schedules for this zone
                        break
            finally:
                shared.logger.debug(self, "CheckAndActivateZones - Releasing lock: nextRunSchedule")
                shared.lockNextRunSchedule.release()
                    
            
            if rebuildSchedule is True:
                shared.logger.debug(self, "A zone was evaluated. Schedule needs to be updated.")
                Scheduler.nextRunScheduleIsDirty = True

            # Reset the evaluating zones flag so someone else can evaluate it next time.
            self.evaluatingZones = False
    


    def heartbeat(self):
        shared.logger.debug(self, "\n\n========================= HEARTBEAT START =========================\n\n")
        
        self.checkAndActivateZones()
        self.checkAndDeactivateZones()

        # Run the heartbeat every minute
        threading.Timer(60, self.heartbeat).start()

    def meetsTemperatureConditions(self, temperature_bo, decisionEvent):

        # shared.logger.debug(self,vars(temperature_bo))

        if temperature_bo.enabled == True:
            # current_temp = getCurrentTemp()
            shared.logger.debug(self,"Temperature Check Enabled. Evaluation if --> " + str(temperature_bo.lower_limit ) + "<=" + str(self.getCurrentTemp()) + " <= " + str(temperature_bo.upper_limit))
            decisionEvent.temperature_enabled = True
            decisionEvent.temperature_lower_limit = temperature_bo.lower_limit
            decisionEvent.temperature_upper_limit = temperature_bo.upper_limit
            decisionEvent.current_temperature = self.getCurrentTemp()
                
            if  self.getCurrentTemp() <temperature_bo.lower_limit:
                shared.logger.debug(self,"Temperature is BELOW lower limit. Will not activate.")
                decisionEvent.reason = EnumReasonCodes.TemperatureBelowMin
                decisionEvent.decision = EnumDecisionCodes.DontActivateZone
                return False
            elif  self.getCurrentTemp() > temperature_bo.upper_limit:
                shared.logger.debug(self,"Temperature is ABOVE max limit. Will not activate")
                decisionEvent.reason = EnumReasonCodes.TemperatureAboveMax
                decisionEvent.decision = EnumDecisionCodes.DontActivateZone
        else:
            decisionEvent.temperature_enabled = False


        return True

    def meetsRainConditions(self, rain_rule, decisionEvent):

        if rain_rule.enabled == True:
            shared.logger.debug(self,"Rain Check Enabled. 3 hour check . Is " + str(self.getShortTermRain()) + "<= " + str(rain_rule.short_term_limit ))
            shared.logger.debug(self,"Rain Check Enabled. 24 hour check . Is " + str(self.getDailyRain()) + "<= " + str(rain_rule.daily_limit ))
            
            decisionEvent.rain_enabled = True
            decisionEvent.rain_short_term_limit = rain_rule.short_term_limit
            decisionEvent.rain_daily_limit = rain_rule.daily_limit
            decisionEvent.current_3hour_forecast = self.getShortTermRain()
            decisionEvent.current_daily_forecast = self.getDailyRain()

            if self.getShortTermRain() > rain_rule.short_term_limit:

                shared.logger.debug(self,"Short term rain rule FAILED. Will not activate.")
                decisionEvent.reason = EnumReasonCodes.ShortTermRainExpected
                decisionEvent.decision = EnumDecisionCodes.DontActivateZone
                return False
            elif self.getDailyRain() > rain_rule.daily_limit:
                shared.logger.debug(self,"Daily  rain rule FAILED. Will not activate.")
                decisionEvent.reason = EnumReasonCodes.LongTermRainExpected
                decisionEvent.decision = EnumDecisionCodes.DontActivateZone
                return False    
        else:
            decisionEvent.rain_enabled = False
                
            

        # Current = 3 hours
        # Daily = 24 hours
        return True

    def getWeatherProfile(self):

        if self.weather_profile is None or self.weather_profile_is_old:
            
            # Create a settings retriever
            city = self.settingsManager.getCity()
            country = self.settingsManager.getCountry()

            shared.logger.debug(self,"need to retrieve new weather profile")
            self.weather_profile = self.weather_centre.createWeatherProfile(city, country)

            # shared.logger.debug(self,vars(self.weather_profile))
            # We got a new profile, so reset the "old" flag
            self.weather_profile_is_old = False
            
            
            # After 10 minutes, the weather profile will be invalidated.
            threading.Timer(60*10, self.markWeatherProfileAsDirty).start()
        
        return self.weather_profile

    def markWeatherProfileAsDirty(self):
        self.weather_profile_is_old = True

    def getCurrentTemp(self):
        return self.getWeatherProfile().currentProfile.temperature.current
    
    def getShortTermRain(self):
        return self.getWeatherProfile().currentProfile.rainAmount
    
    def getDailyRain(self):
        return self.getWeatherProfile().twentyfourhourProfile.rainAmount
    
    
    

    





    