from service.weather_hub.weather_center import WeatherCenter
from service.utilities.conversion import Conversions
from service.zone.zone_timing_bo import ZoneTiming
from service.database.decision_dbo import DecisionDBO
from service.core.scheduler import Scheduler
from service.zone.zone_controller import ZoneController
from service.core import shared, shared_events
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
    weather_snapshot = None
    evaluatingZones = False
    activeZones = []
    

    def __init__(self):
        
        self.scheduler = Scheduler()
        self.decisionHistoryDBO = DecisionDBO()
        self.zone_controller = ZoneController()
        self.weather_centre = WeatherCenter()
        self.settingsManager = SettingsManager()
        self.engineLastRan = None
        self.weather_snapshot = None
        NotifierEngine()
        self.timer = None
        self.start()
    
        
    def getEngineLastRan(self):
        return self.engineLastRan

    def start(self):

        shared.logger.info(self, "Heartbeat has been started")
        self.heartbeat()
    
    def stop(self):
        shared.logger.info(self, "Heartbeat has been stopped")
        # Before shutting ourself down, let's stop any zones that are running
        self.zone_controller.deactivateAllZones();
        self.timer.cancel()




    
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

            try:

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
                            decisionEvent = DecisionHistory(zone_id=zonetiming.zone.id, event_time=currentDateTime, start_time=zonetiming.start_time, end_time=zonetiming.end_time)
                            # decisionEvent = DecisionHistory()
                            shared.logger.debug(self, "Current Time within boundries")
                            
                            #Check conditions
                            tempRuleMet = self.meetsTemperatureConditions(zonetiming.zone.temperature_rule, decisionEvent)
                            
                            if(decisionEvent.reason is None or decisionEvent.reason != EnumReasonCodes.FailedToGetWeatherData):
                                rainRuleMet = self.meetsRainConditions(zonetiming.zone.rain_rule, decisionEvent)
                            
                            activateZone = tempRuleMet * rainRuleMet
                            
                            if activateZone:
                                # Copy the zone timing object to the active running zones
                                self.zone_controller.activateZone(zonetiming, decisionEvent, EnumReasonCodes.AllConditionsPassed)
                            else:

                                shared.logger.debug(self, "Going to log decision event")
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
            finally:
                # Reset the evaluating zones flag so someone else can evaluate it next time.
                self.evaluatingZones = False
    


    def heartbeat(self):
        
        try:
            shared.logger.debug(self, "\n\n========================= HEARTBEAT START =========================\n\n")
            self.engineLastRan = datetime.now()
            self.checkAndActivateZones()
            self.checkAndDeactivateZones()
        except Exception as e:
            shared.logger.error(self, "Heartbeat caught an exception")
            errMsg= "Exception: " + repr(e)
            shared.logger.error(self, errMsg)
            #raise #Comment this out for prod
            
        finally:
            # Run the heartbeat every minute
            shared.logger.debug(self, "Scheduling timer for 1 minute from now")
            self.timer = threading.Timer(60, self.heartbeat)
            self.timer.start()
        

        
        

    def meetsTemperatureConditions(self, temperature_bo, decisionEvent):

        # shared.logger.debug(self,vars(temperature_bo))

        if temperature_bo.enabled == True:
            # current_temp = getCurrentTemp()
            shared.logger.debug(self,"Temperature Check Enabled. Evaluation if --> " + str(temperature_bo.lower_limit ) + "<=" + str(self.getCurrentTemp()) + " <= " + str(temperature_bo.upper_limit))
            decisionEvent.temperature_enabled = True
            decisionEvent.temperature_lower_limit = temperature_bo.lower_limit
            decisionEvent.temperature_upper_limit = temperature_bo.upper_limit
            decisionEvent.current_temperature = self.getCurrentTemp()
            
            if self.getCurrentTemp() == 9999:
                shared.logger.debug(self,"Temperature is 9999. Will not activate due to API failure.")
                
                decisionEvent.reason = EnumReasonCodes.FailedToGetWeatherData
                shared.logger.debug(self,"Set reason code as failed to get weather data")
                
                decisionEvent.decision = EnumDecisionCodes.DontActivateZone
                shared.logger.debug(self,"Set decision as do not activate")
                return False
            elif  self.getCurrentTemp() <temperature_bo.lower_limit:
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

            if self.getShortTermRain() == 9999 or self.getDailyRain() == 9999:
                decisionEvent.reason = EnumReasonCodes.FailedToGetWeatherData
                decisionEvent.decision = EnumDecisionCodes.DontActivateZone
                return False
            elif self.getShortTermRain() > rain_rule.short_term_limit:

                shared.logger.debug(self,"Short term rain rule FAILED. Will not activate. " + str(self.getShortTermRain()) + " > " + str(rain_rule.short_term_limit))
                decisionEvent.reason = EnumReasonCodes.ShortTermRainExpected
                decisionEvent.decision = EnumDecisionCodes.DontActivateZone
                return False
            elif self.getDailyRain() > rain_rule.daily_limit:
                shared.logger.debug(self,"Daily rain rule FAILED. Will not activate " + str(self.getDailyRain()) + " > " + str(rain_rule.daily_limit))
                decisionEvent.reason = EnumReasonCodes.LongTermRainExpected
                decisionEvent.decision = EnumDecisionCodes.DontActivateZone
                return False    
        else:
            decisionEvent.rain_enabled = False
                
            

        # Current = 3 hours
        # Daily = 24 hours
        return True

    def getWeatherSnapshot(self):
        shared.logger.debug(self, "getWeatherSnapshot invoked")

        if self.weather_snapshot is None or self.weather_snapshot_is_old:
            
            # Create a settings retriever
            city = self.settingsManager.getCity()
            country = self.settingsManager.getCountry()

            shared.logger.debug(self,"Need to retrieve new weather snapshot")
            self.weather_snapshot = self.weather_centre.createWeatherSnapshot(city, country)

            #If the weather snapshot is None, it means it failed to retrieve from the API,
            # so we set the reset timers accordingly (30 if we hit the API, 1 if we didn't)
            if self.weather_snapshot.currentForecast is not None:
                # After 30 minutes, the weather snapshot will be invalidated.
                shared.logger.debug(self, "Retrieved weather profile. Setting dirty timer for 30 minutes")
                threading.Timer(60*30, self.markWeatherProfileAsDirty).start()
            else:
                shared.logger.debug(self, "failed to retrieve weather profile. Setting dirty timer for 1 minute")
                
                # After 1 minutes, the weather API will be retried
                threading.Timer(60*1, self.markWeatherProfileAsDirty).start()

            self.weather_snapshot_is_old = False

        return self.weather_snapshot

    def markWeatherProfileAsDirty(self):
        shared.logger.debug(self, "Marking the weather forecast as old. Will fetch a new one on next heartbeat")
        self.weather_snapshot_is_old = True

    def getCurrentTemp(self):
        if self.getWeatherSnapshot().currentForecast is None:
            return 9999

        return self.getWeatherSnapshot().currentForecast.temperature.current
    
    def getShortTermRain(self):
        if self.getWeatherSnapshot().currentForecast is None:
            return 9999

        return self.getWeatherSnapshot().currentForecast.rainAmount
    
    def getDailyRain(self):
        if self.getWeatherSnapshot().twentyfourhourForecast is None:
            return 9999

        return self.getWeatherSnapshot().twentyfourhourForecast.rainAmount
    
    
    

    





    