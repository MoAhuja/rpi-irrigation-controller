from service.zone.zone_manager import ZoneManager
from service.weather_hub.weather_center import WeatherCenter
from service.zone.zone_controller import ZoneController
from service.utilities.conversion import Conversions
from service.zone.zone_timing_bo import ZoneTiming
from service.database.decision_dbo import DecisionDBO
from service.scheduler import Scheduler

# Not sure i should be accessing DAO's at this layer, but it seems unneccessary to create a new object to track the same data
from service.database.db_schema import DecisionHistory, EnumDecisionCodes, EnumReasonCodes

# from pprint import pprint
from datetime import datetime
from service.utilities.logger import Logger
import threading

class Engine():

    zone_manager = None
    decisionHistoryDBO = None
    zone_controller = None
    weather_centre = None
    weather_profile = None
    evaluatingZones = False
    activeZones = []
    

    def __init__(self, event_publisher):
        
        # Register for notifications 
        event_publisher.register(self)
        self.zone_manager = ZoneManager()
        self.scheduler = Scheduler()
        self.decisionHistoryDBO = DecisionDBO()
        self.zone_controller = ZoneController()
        self.activeZones = {}
        self.weather_centre = WeatherCenter()
        self.heartbeat()
        

    def manuallyActivateZone(self, zone, end_time):
        # TODO: Check if the zone is already active
        # TODO: This call should come from the zone manager (or some other place after validation). The user should not interface with the engine directly.
        # TODO: Inject this zone into list of active zones
        # TODO: Add decision history as "manual"
        # TODO: Add activation to history table
        # TODO: Tell controller to start the zone
        return False
    

    
    def manuallyDeactivateZone(self, zone):

        # Check if zone is in the list of active zones
        if self.activeZones[zone.id] is not None:
            # TODO: What if a manual deactiate is called while he zone list is being?? Will this crash it?
            del self.activeZones[zone.id]
            Logger.info(self,"Zone " + str(zone.id) + "has been MANUALLY deactivated")

            # TODO: insert a deactivation history event
        

   

    
    # Need to listen for changes
    def publishZoneInfoUpdated(self):
        # We received an event the zone info was updated. We need to drop our list.
        self.isDirty = True 
    
    def deactivateAllZones(self):
        Logger.debug(self,"Deactivating All Zones")
        for key, activeZone in self.activeZones.items():
            Logger.debug(self, "Deactivating -> " + key + "-->" + value.zone.name)
            self.zone_controller.deactivateZone(activeZone.zone)
        
        # Reset back to an empty hashmap
        self.activeZones = {}

    def checkAndDeactivateZones(self):
        deactivateList = []

        
        # Loop through the activeZones list and check if the end time has been past
        Logger.debug(self,"Checking if any zones need to be deactivated")
        currentTime = datetime.now().time()

        for key, activeZone in self.activeZones.items():
            dh =  DecisionHistory()

            Logger.debug(self,"Deactivation Check: [Zone ID] = " + str(key) + ", [CurrentTime] = " + Conversions.convertDBTimeToHumanReadableTime(currentTime)+ ", [Deactivation Time] =  " + Conversions.convertDBTimeToHumanReadableTime(activeZone.end_time))
            if currentTime > activeZone.end_time:
                dh.zone = activeZone.zone
                dh.start_time = activeZone.start_time
                dh.end_time = activeZone.end_time
                dh.decision = EnumDecisionCodes.DeactivateZone
                dh.reason = EnumReasonCodes.AllConditionsPassed

                self.decisionHistoryDBO.insertDecisionEvent(dh)
                
                Logger.debug(self, "Zone will be deactivated")
                # Add to list so we can remove it from our list of active zones
                deactivateList.append(key)

                # Deactivate it
                self.zone_controller.deactivateZone(activeZone.zone)

        Logger.debug(self,"Deactivation check complete")
        
        for x in deactivateList:
            del self.activeZones[x]

    def checkAndActivateZones(self):
        
        Logger.debug(self,"Evaluating Zones == " + str(self.evaluatingZones))

        # We need to make sure no one else is looping through the zones in case this gets invoked on another thread
        if self.evaluatingZones is False:

            Logger.debug(self,"Evaluating zones")
            # Set a flag indicating the zones are being evaluated
            self.evaluatingZones = True

            # Load the zones that we need to monitor
            self.scheduler.loadNextRunSchedule()

            Logger.debug(self,"Finished loading zones")

            # Get Time
            currentDateTime = datetime.now()
            currentTime = currentDateTime.time()
            Logger.debug(self, "Current Time is: " + Conversions.convertDBTimeToHumanReadableTime(currentTime))
            currentTemp = self.getCurrentTemp()
            Logger.debug(self, "Current Temperature is: " + str(currentTemp))
            
            # Foreach enabled zone
            # Logger.debug(self, "There are " + str(len(self.enabledZones)) + " enabled zones")
            
            rebuildSchedule = False

            for id, zonetiming in self.scheduler.nextRunSchedule.items():
                
                Logger.debug(self, "Evaluating Zone: " + zonetiming.zone.name)

                # Check if this zone is already active
                # TODO: What do we do if two schedules overlap? I suppose they can't? Need to make sure of this.
                # TODO: If they can't overlap, then we likely don't need this.
                if id in self.activeZones:
                    Logger.debug(self,"Zone already active. Skipping evaluation.")
                    break

                # Reset all the conditions
                rainRuleMet = False
                tempRuleMet = False
            
                Logger.debug(self, "Activate if: " + str(zonetiming.start_time) + " < " + str(currentDateTime)  + " < " + str(zonetiming.end_time))
                # Check if the current time is past the start time, but before the end time
                if zonetiming.start_time <= currentDateTime < zonetiming.end_time:

                    # Create a decision event w/ current info
                    decisionEvent = None
                    decisionEvent = DecisionHistory(zone=zone, event_time=currentDateTime, start_time=sch.start_time, end_time=sch.end_time)
                
                    Logger.debug(self, "Current Time within boundries")
                    
                    #Check conditions
                    tempRuleMet = self.meetsTemperatureConditions(zone.temperature_rule, decisionEvent)
                    rainRuleMet = self.meetsRainConditions(zone.rain_rule, decisionEvent)
                    
                    activateZone = tempRuleMet * rainRuleMet
                    
                    if activateZone:
                        # Copy the zone timing object to the active running zones
                        self.activateZone(zonetiming)
                        decisionEvent.decision = EnumDecisionCodes.ActivateZone
                        decisionEvent.reason = EnumReasonCodes.AllConditionsPassed
                        
                        # Set flag indicating the schedule needs to be re-built
                        rebuildSchedule = True

                        #TODO: Update the next run schedule for the zone timing object that was started
                        # self.scheduler.updateNextRunForZone(zonetiming.zone)

                    #Log an event, if one is available to be logged.
                    self.decisionHistoryDBO.insertDecisionEvent(decisionEvent)
                    self.decisionHistoryDBO.saveAndClose()

                    # Since the current time can only fall in one schedule, we can stop evaluating
                    # schedules for this zone
                    break
                            
            
            if rebuildSchedule is True:
                Logger.debug(self, "A zone was activated. Schedule needs to be updated.")
                self.nextRunScheduleIsDirty = True

            # Reset the evaluating zones flag so someone else can evaluate it next time.
            self.evaluatingZones = False
    
    def activateZone(self, zonetimingObj):

        Logger.debug(self,"Adding zone '" + zone.name + "' to list of active zones")
        # add this zone to a list of activated zones
        self.activeZones[zonetimingObj.zone.id] = zonetimingObj

        Logger.debug(self,"Activating Zone")

        # call the zone controller and activate the zone
        self.zone_controller.activateZone(zonetimingObj.zone)

    def heartbeat(self):
        Logger.debug(self, "\n\n========================= HEARTBEAT START =========================\n\n")
        
        self.checkAndActivateZones()
        self.checkAndDeactivateZones()

        # Run the heartbeat every minute
        threading.Timer(10, self.heartbeat).start()

    def meetsTemperatureConditions(self, temperature_bo, decisionEvent):

        # Logger.debug(self,vars(temperature_bo))

        if temperature_bo.enabled == True:
            # current_temp = getCurrentTemp()
            Logger.debug(self,"Temperature Check Enabled. Evaluation if --> " + str(temperature_bo.lower_limit ) + "<=" + str(self.getCurrentTemp()) + " <= " + str(temperature_bo.upper_limit))
            decisionEvent.temperature_enabled = True
            decisionEvent.temperature_lower_limit = temperature_bo.lower_limit
            decisionEvent.temperature_upper_limit = temperature_bo.upper_limit
            decisionEvent.current_temperature = self.getCurrentTemp()
                
            if  self.getCurrentTemp() <temperature_bo.lower_limit:
                Logger.debug(self,"Temperature is BELOW lower limit. Will not activate.")
                decisionEvent.reason = EnumReasonCodes.TemperatureBelowMin
                decisionEvent.decision = EnumDecisionCodes.DontActivateZone
                return False
            elif  self.getCurrentTemp() > temperature_bo.upper_limit:
                Logger.debug(self,"Temperature is ABOVE max limit. Will not activate")
                decisionEvent.reason = EnumReasonCodes.TemperatureAboveMax
                decisionEvent.decision = EnumDecisionCodes.DontActivateZone
        else:
            decisionEvent.temperature_enabled = False


        return True

    def meetsRainConditions(self, rain_rule, decisionEvent):

        if rain_rule.enabled == True:
            Logger.debug(self,"Rain Check Enabled. 3 hour check . Is " + str(self.getShortTermRain()) + "<= " + str(rain_rule.short_term_limit ))
            Logger.debug(self,"Rain Check Enabled. 24 hour check . Is " + str(self.getDailyRain()) + "<= " + str(rain_rule.daily_limit ))
            
            decisionEvent.rain_enabled = True
            decisionEvent.rain_short_term_limit = rain_rule.short_term_limit
            decisionEvent.rain_daily_limit = rain_rule.daily_limit
            decisionEvent.current_3hour_forecast = self.getShortTermRain()
            decisionEvent.current_daily_forecast = self.getDailyRain()

            if self.getShortTermRain() > rain_rule.short_term_limit:

                Logger.debug(self,"Short term rain rule FAILED. Will not activate.")
                decisionEvent.reason = EnumReasonCodes.ShortTermRainExpected
                decisionEvent.decision = EnumDecisionCodes.DontActivateZone
                return False
            elif self.getDailyRain() > rain_rule.daily_limit:
                Logger.debug(self,"Daily  rain rule FAILED. Will not activate.")
                decisionEvent.reason = EnumReasonCodes.LongTermRainExpected
                decisionEvent.decision = EnumDecisionCodes.DontActivateZone
                return False    
        else:
            decisionEvent.rain_enabled = False
                
            

        # Current = 3 hours
        # Daily = 24 hours
        return True

    def getWeatherProfile(self):

        # TODO: Mississauga, CA shouldn't be hardcoded. We need a "System config section"
        if self.weather_profile is None or self.weather_profile_is_old:
            
            Logger.debug(self,"need to retrieve new weather profile")
            self.weather_profile = self.weather_centre.createWeatherProfile("Mississauga", "CA")

            # Logger.debug(self,vars(self.weather_profile))
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
    
    
    

    





    