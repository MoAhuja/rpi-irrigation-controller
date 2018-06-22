from service.zone.zone_manager import ZoneManager
from service.database.db_schema import EnumScheduleType
from datetime import datetime, timedelta

class Scheduler():

    def buildNextRunSchedule():

        nextRunHash = {}

        # create a zone manager instance
        zm = ZoneManager()

        # Retrieve all enables zones
        enabledZones = zm.retrieveAllEnabledZones()
        # retrieve AllEnablesZones

        for zone in enabledZones:

            # Get the current time
            currentTime = datetime.now()
            currentDow = datetime.today().weekday()

            # Setup some arbitrary value in the past
            nextRunDatetime = datetime.now() - timedelta(days=2)

            # Cycle through each schedule
            for sch in zone.schedules:

                if sch.schedule_type is EnumScheduleType.DayAndTime:
                    scheduledTime = sch.start_time

                    # Cycle through each day and create the next run date
                    for day in sch.days:

                        # Figure out how many days ahead of the current day the schedule is.
                        addDays = day.dayOfWeek - currentDow

                        # if the value is negative, then it means the day was before the current day of week, so we need toa dd
                        # 7 days to cycle to the next week
                        if(addDays < 0):
                            addDays = addDays + 7
                        
                        # Create the water time based on the number of days to add
                        scheduledWatertime = currentTime() + timedelta(days=addDays)

                        # Replace hours and minutes using the value from the schedule object
                        hour, minute = sch.getHoursAndMinutesFromStartTime()
                        scheduledWatertime = scheduledWatertime.replace(hour=hour, minute=minute)

                        # Compare this water time against the lowest value stored. Replace if lower.
                        Logger.debug("Comparing " + str(scheduledWatertime) + " against " + str(nextRunDatetime))
                        if scheduledWaterTime < nextRunDatetime:
                            nextRunDatetime = scheduledWatertime

                    # get sch.dow
                        # addDays = sch.dow - currentDow
                        # if addDays < 0, add 7

                        # create new time of currentDate + addDays & replace time with sch.hour/time
                        
                        newDate = date.replace(hour=sch.hour, minutes=sch.minutes)


            # if type == DOW
                # if first time, insert dow & time as next run (temp[dow])
                # else
                    # if sch.dow == currentDow
                        # evaluate time & if it's less than temp[dow]
                    # else if currentDow < sch.dow < temp[dow]
                        # replace temp[dow] with sch.dow
                    


