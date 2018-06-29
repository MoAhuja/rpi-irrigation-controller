from service.database.db_schema import EnumScheduleType
from datetime import datetime, timedelta
from service.utilities.logger import Logger
from service.zone.zone_timing_bo import ZoneTiming
from service import shared
from service import shared_events
from service.zone.zone_data_manager import ZoneDataManager
from service.system.settings_manager import SettingsManager

class Scheduler():

    nextRunSchedule = None
    nextRunScheduleIsDirty = True

    def __init__(self):
        # Listen for zone or rain delay updates only
        shared_events.event_publisher.register(self, True, True, False, False)

        self.settingsManager = SettingsManager()
        self.nextRunSchedule = {}
        self.nextRunScheduleIsDirty = True
        self.loadNextRunSchedule()


    # Listen for zone updated events
    def eventZoneUpdated(self):
        shared.logger.debug(self, "Received event: Zone Info updated")
        # Mark the schedule as dirty
        # TODO: Change this to listen for schedule updated events
        self.nextRunScheduleIsDirty = True

    def eventRainDelayUpdated(self):

        shared.logger.debug(self, "Received event: Rain delay updated")
        # Mark the schedule as dirty
        # TODO: Change this to listen for schedule updated events
        self.nextRunScheduleIsDirty = True

    def loadNextRunSchedule(self):
        
        shared.logger.debug(self, "load next run schedule entered. Next run schedule dirty = " + str(self.nextRunScheduleIsDirty))

        # Check if zone data needs to be reloaded
        if self.nextRunScheduleIsDirty is True or self.nextRunSchedule is None:
            # Because the zones may have changed, we're going to force shutoff all the zones
            # and allow them to re-activate if required
            shared.logger.debug(self, "Next run schedule is dirty. Going to obtain updated data")

            self.buildNextRunSchedule()
            self.nextRunScheduleIsDirty = False
    
    def schedulerIsDirty(self):
        self.nextRunScheduleIsDirty = True
    
    # Need to listen for changes
    def publishZoneInfoUpdated(self):
        # We received an event the zone info was updated. We need to drop our list.
        self.nextRunScheduleIsDirty = True

    # Builds the schedule and stores it in the class instance
    def buildNextRunSchedule(self):
       
        # create a zone manager instance
        zm = ZoneDataManager()

        # Retrieve all enables zones
        enabledZones = zm.retrieveAllEnabledZones()
        
        rainDelayInHours = self.settingsManager.getRainDelay()
        print("Rain Delay set to: " + str(rainDelayInHours))

        # Get the current time
        referenceTime = datetime.now() + timedelta(hours=int(rainDelayInHours))

        print("Reference time = " + str(referenceTime))

        # currentDow = datetime.today().weekday()
        currentDow = referenceTime.weekday()

        print("Current DOW = " + str(currentDow))


        for zone in enabledZones:

            shared.logger.debug(self, "Building next run for Zone " + zone.name)

            # Setup some arbitrary value in the past
            nextRunDatetime = datetime.now() + timedelta(days=30)

            shared.logger.debug(self, "BuildNextRunSchedule - Waiting for lock: nextRunSchedule")
            shared.lockNextRunSchedule.acquire()

            try:
                # Cycle through each schedule
                for sch in zone.schedules:

                    # NEed to check if the schedule is enabled, first
                    if sch.enabled is False:
                        shared.logger.debug("Schedule is not enabled. Skipping.")
                        break

                    if sch.schedule_type is EnumScheduleType.DayAndTime:
                        scheduledTime = sch.start_time
                        shared.logger.debug(self, "start time == " + str(scheduledTime))
                        shared.logger.debug(self, "end time == " + str(sch.end_time))

                        hour, minute = sch.getHoursAndMinutesFromStartTime()
                        
                        shared.logger.debug(self, "hours and minutes of start time == " + str(hour) + ":" + str(minute))

                        # Cycle through each day and create the next run date
                        for day in sch.days:

                            shared.logger.debug(self, "Evaluating: " + day.dayOfWeek.name + " @ " + str(scheduledTime))
                            # Figure out how many days ahead of the current day the schedule is.
                            addDays = day.dayOfWeek.value - currentDow

                            # if the value is negative, then it means the day was before the current day of week, so we need toa dd
                            # 7 days to cycle to the next week
                            if(addDays < 0):
                                addDays = addDays + 7
                            # If the scheduled day == the current day, we need to check if the times to see if we're
                            # too late and have to schedule it for next week
                            elif addDays is 0:
                                if scheduledTime < referenceTime.time():
                                    addDays = addDays + 7
                            
                            # Create the water time based on the number of days to add
                            scheduledWatertime = referenceTime + timedelta(days=addDays)

                            # Replace hours and minutes using the value from the schedule object
                            scheduledWatertime = scheduledWatertime.replace(hour=hour, minute=minute, second=0)

                            # Compare this water time against the lowest value stored. Replace if lower.
                            shared.logger.debug(self, "Comparing " + str(scheduledWatertime) + " against " + str(nextRunDatetime))
                            if referenceTime < scheduledWatertime < nextRunDatetime:
                                nextRunDatetime = scheduledWatertime
                                nextRunDuration = sch.getDuration()
                                shared.logger.debug(self, "Setting this as the temporary next run time")



                shared.logger.info(self, "Next run date for Zone " + zone.name +  " is " + str(nextRunDatetime))
                
                # Calculate the end time
                endTime = self.calculateEndTime(zone, nextRunDatetime, nextRunDuration)
                shared.logger.info(self, "Next run end time for Zone " + zone.name + " is " + str(endTime))

                # Set the hashmap
                self.nextRunSchedule[zone.id] = ZoneTiming.initialize(zone, nextRunDatetime, endTime)
            finally:
                shared.lockNextRunSchedule.release()
                shared.logger.debug(self, "BuildNextRunSchedule - Released lock: nextRunSchedule")
            
    def calculateEndTime(self, zone, start_time, duration):
        return start_time + duration


