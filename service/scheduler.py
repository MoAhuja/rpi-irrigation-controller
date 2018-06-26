from service.zone.zone_manager import ZoneManager
from service.database.db_schema import EnumScheduleType
from datetime import datetime, timedelta
from service.utilities.logger import Logger
from service.zone.zone_timing_bo import ZoneTiming

class Scheduler():

    nextRunSchedule = {}
    nextRunScheduleIsDirty = True

    def __init__(self):
        # checks if
        nextRunScheduleIsDirty = True
        self.loadNextRunSchedule()

    def loadNextRunSchedule(self):
        
        Logger.debug(self, "load next run schedule entered. Next run schedule dirty = " + str(self.nextRunScheduleIsDirty))

        # Check if zone data needs to be reloaded
        if self.nextRunScheduleIsDirty is True or self.nextRunSchedule is None:
            # Because the zones may have changed, we're going to force shutoff all the zones
            # and allow them to re-activate if required
            Logger.debug(self, "Next run schedule is dirty. Going to obtain updated data")

            self.buildNextRunSchedule()
            self.nextRunScheduleIsDirty = False
    
    def schedulerIsDirty(self):
        self.nextRunScheduleIsDirty = True

    # Builds the schedule and stores it in the class instance
    def buildNextRunSchedule(self):

        # create a zone manager instance
        zm = ZoneManager()

        # Retrieve all enables zones
        enabledZones = zm.retrieveAllEnabledZones()
        # retrieve AllEnablesZones

        # Get the current time
        currentTime = datetime.now()
        currentDow = datetime.today().weekday()


        for zone in enabledZones:

            Logger.debug(self, "Building next run for Zone " + zone.name)

            # Setup some arbitrary value in the past
            nextRunDatetime = datetime.now() + timedelta(days=10)

            # Cycle through each schedule
            for sch in zone.schedules:

                # NEed to check if the schedule is enabled, first
                if sch.enabled is False:
                    Logger.debug("Schedule is not enabled. Skipping.")
                    break

                if sch.schedule_type is EnumScheduleType.DayAndTime:
                    scheduledTime = sch.start_time
                    Logger.debug(self, "start time == " + str(scheduledTime))
                    Logger.debug(self, "end time == " + str(sch.end_time))

                    hour, minute = sch.getHoursAndMinutesFromStartTime()
                    
                    Logger.debug(self, "hours and minutes of start time == " + str(hour) + ":" + str(minute))

                    # Cycle through each day and create the next run date
                    for day in sch.days:

                        Logger.debug(self, "Evaluating: " + day.dayOfWeek.name + " @ " + str(scheduledTime))
                        # Figure out how many days ahead of the current day the schedule is.
                        addDays = day.dayOfWeek.value - currentDow

                        # if the value is negative, then it means the day was before the current day of week, so we need toa dd
                        # 7 days to cycle to the next week
                        if(addDays < 0):
                            addDays = addDays + 7
                        # If the scheduled day == the current day, we need to check if the times to see if we're
                        # too late and have to schedule it for next week
                        elif addDays is 0:
                            if scheduledTime < currentTime.time():
                                addDays = addDays + 7
                        
                        # Create the water time based on the number of days to add
                        scheduledWatertime = currentTime + timedelta(days=addDays)

                        # Replace hours and minutes using the value from the schedule object
                        
                        scheduledWatertime = scheduledWatertime.replace(hour=hour, minute=minute, second=0)

                        # Compare this water time against the lowest value stored. Replace if lower.
                        Logger.debug(self, "Comparing " + str(scheduledWatertime) + " against " + str(nextRunDatetime))
                        if currentTime < scheduledWatertime < nextRunDatetime:
                            nextRunDatetime = scheduledWatertime
                            nextRunDuration = sch.getDuration()
                            Logger.debug(self, "Setting this as the temporary next run time")



            Logger.info(self, "Next run date for Zone " + zone.name +  " is " + str(nextRunDatetime))
            
            # Calculate the end time
            endTime = self.calculateEndTime(zone, nextRunDatetime, nextRunDuration)
            Logger.info(self, "Next run end time for Zone " + zone.name + " is " + str(endTime))

            # Set the hashmap
            self.nextRunSchedule[zone.id] = ZoneTiming.initialize(zone, nextRunDatetime, endTime)

    def calculateEndTime(self, zone, start_time, duration):
        return start_time + duration


