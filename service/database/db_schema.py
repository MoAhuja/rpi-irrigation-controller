import os
import sys
from sqlite3 import Connection as SQLite3Connection
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Time, DateTime, event, Enum, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from pprint import pprint
from datetime import datetime
from service.utilities.conversion import Conversions
import enum
 
# TODO: Split the schema into separate files??
Base = declarative_base()

class Zone(Base):
    __tablename__ = 'zone'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(250), nullable=False,  unique=True)
    description = Column('description', String(250), nullable=True)
    enabled = Column('enabled', Boolean, default=True)

    # environment = relationship("EnvironmentRules", uselist=False, back_populates="zone")
    temperature_rule = relationship("TemperatureRule", uselist=False, back_populates="zone")
    rain_rule=relationship("RainRule", uselist=False, back_populates="zone")
    schedules = relationship("Schedule", uselist=True, back_populates="zone")
    pin_config = relationship("RpiPinMapper", uselist=False, back_populates="zone")

    # TODO: do we want to back-populate this? It's going to be a ton of data to load even if we don't need it
    decision_history = relationship("DecisionHistory", uselist=True, back_populates="zone")
    
    @classmethod
    def initializeWithJSON(cls, jsonData):

        cl = cls()

        cl.description=jsonData["input_zone_description"]
        cl.name=jsonData["input_zone_name"]
        cl.enabled=True
        
        cl.temperature = TemperatureRule.initializeWithJSON(jsonData["temperature"], cl)
        cl.rain = RainRule.initializeWithJSON(jsonData["rain"], cl)
        
        for schedule in jsonData["schedule"]:
            cl.schedules.append(Schedule.initializeWithJSON(schedule, cl))

        return cl

class TemperatureRule(Base):
    __tablename__ = 'temperature_rules'
    id = Column('id', Integer, primary_key=True)
    # environment_id = Column('environment_id', Integer, ForeignKey('environment_rules.id'), nullable=False)
    enabled = Column('enabled', Boolean, default=False)
    lower_limit = Column('lower_limit', Integer, default=0)
    upper_limit = Column('upper_limit', Integer, default=0)
    # zone = relationship(EnvironmentRules, back_populates="temperature_rule")

    zone_id = Column('zone_id', Integer, ForeignKey('zone.id'), nullable=False)
    zone=relationship("Zone", back_populates="temperature_rule")

    @classmethod
    def initializeWithJSON(cls, jsonData, zone):
        cl = cls()
        cl.lower_limit = jsonData["min"]
        cl.upper_limit = jsonData["max"]
        cl.enabled = True
        cl.zone = zone
        # TODO: make this dynamic??

        return cl

class RainRule(Base):
    __tablename__ = 'rain_rules'
    id = Column('id', Integer, primary_key=True)
    # environment_id = Column('environment_id', Integer, ForeignKey('environment_rules.id'), nullable=False)
    enabled = Column('enabled', Boolean, default=False)
    short_term_limit = Column('short_term_limit', Integer, default=0)
    daily_limit = Column('daily_limit', Integer, default=0)
    # environment = relationship(EnvironmentRules, back_populates="rain_rule")

    zone_id = Column('zone_id', Integer, ForeignKey('zone.id'), nullable=False)
    zone=relationship("Zone", back_populates="rain_rule")
    
    @classmethod
    def initializeWithJSON(cls, jsonData, zone):
        cl = cls()
        cl.short_term_limit = jsonData["shortTermExpectedRainAmount"]
        cl.daily_limit = jsonData["dailyExpectedRainAmount"]
        cl.enabled = True
        cl.zone = zone

        return cl

class EnumScheduleType(enum.Enum):
    DayAndTime = 0
    TimeAndFrequency= 1

class Schedule(Base):
    __tablename__ = 'schedule'
    id = Column('id', Integer, primary_key=True)
    schedule_type = Column('schedule_type', Enum(EnumScheduleType), nullable=False)
    start_time = Column('start_time', Time, nullable=False)
    end_time = Column('end_time', Time, nullable=False)
    enabled = Column('enabled', Boolean, default=False)
    zone_id = Column('zone_id', Integer, ForeignKey('zone.id'), nullable=False)
    zone=relationship("Zone", back_populates="schedules")
    days = relationship("ScheduleDays", uselist=True, back_populates="schedule")

    # @classmethod
    # def initializeWithTimes(cls, iStart, iStop, zone):
    #     cl = cls()
    #     # print("Creating schedule DO")
    #     cl.start_time = Conversions.convertHumanReadableTimetoDBTime(iStart)
    #     cl.end_time = Conversions.convertHumanReadableTimetoDBTime(iStop)
    #     cl.enabled = True
    #     cl.zone = zone

    #     return cl
    
    @classmethod
    def initializeWithJSON(cls, json_data, zone):
        cl = cls()
        # print("Creating schedule DO")
        cl.start_time = Conversions.convertHumanReadableTimetoDBTime(json_data['startTime'])
        cl.end_time = Conversions.convertHumanReadableTimetoDBTime(json_data['endTime'])
        cl.schedule_type = EnumScheduleType(int(json_data["schedule_type"]))
        
        if cl.schedule_type is EnumScheduleType.DayAndTime:
            # Iteratre over each selected day and add it to teh days array
            for val in json_data["days"]:
                cl.days.append(ScheduleDays(dayOfWeek = EnumDayOfWeek(int(val))))

        cl.enabled = True
        cl.zone = zone

        return cl

    def getStartTime(self):
        return Conversions.convertDBTimeToHumanReadableTime(self.start_time)
    
    def getEndTime(self):
         return Conversions.convertDBTimeToHumanReadableTime(self.end_time)
        
    def getHoursAndMinutesFromStartTime(self):
        return self.start_time.hour, self.start_time.minute
    
    def getDuration(self):
        # First we create a datetime object
        now = datetime.now()
        newStart = now.replace(hour=self.start_time.hour, minute=self.start_time.minute)
        newEnd = now.replace(hour=self.end_time.hour, minute=self.end_time.minute)

        return newEnd - newStart

class EnumDayOfWeek(enum.Enum):
    Monday = 0
    Tuesday = 1
    Wednesday = 2
    Thursday =3
    Friday = 4
    Saturday = 5
    Sunday = 6

class ScheduleDays(Base):
    __tablename__ = "schedule_days"
    id = Column('id', Integer, primary_key=True)

    # The main attribute, which day.
    dayOfWeek = Column('day_of_week', Enum(EnumDayOfWeek), nullable=False)

    schedule_id = Column('schedule_id', Integer, ForeignKey('schedule.id'), nullable=False)
    schedule=relationship("Schedule", back_populates="days")
    __table_args__ = (
        UniqueConstraint('schedule_id', 'day_of_week', name='_unique_day_per_schedule'),
        )
    

    

class EnumDecisionCodes(enum.Enum):
    ActivateZone = 0
    DeactivateZone= 1
    DontActivateZone = 2
  

class EnumReasonCodes(enum.Enum):
    AllConditionsPassed = 0
    ShortTermRainExpected = 1
    LongTermRainExpected = 2
    TemperatureBelowMin = 3
    TemperatureAboveMax = 4

# TODO: Complete this event history object (consider rename to "ZoneDecisionHistory")
class DecisionHistory(Base):
    __tablename__ = 'decision_history'
    id = Column('id', Integer, primary_key=True)

    # Map this decision back to a zone
    zone_id = Column('zone_id', Integer, ForeignKey('zone.id'), nullable=False)
    zone=relationship("Zone", back_populates="decision_history") 

    event_time = Column('event_time', DateTime, nullable=False, default=datetime.utcnow)
    
    # Current conditions
    current_temperature = Column('current_temperature', Integer, nullable=True)
    current_3hour_forecast = Column('current_3hour_forecast', Integer, nullable=True)
    current_daily_forecast = Column('current_daily_forecast', Integer, nullable=True)

    
    # Rules in place at time of event
    temperature_enabled = Column('temperature_enabled', Boolean, nullable=True)
    temperature_lower_limit = Column('temperature_lower_limit', Integer, nullable=True)
    temperature_upper_limit = Column('temperature_upper_limit', Integer, nullable=True)
    rain_enabled = Column('rain_enabled', Boolean, nullable=True)
    rain_short_term_limit = Column('rain_short_term_limit', Integer, nullable=True)
    rain_daily_limit = Column('rain_daily_limit', Integer, nullable=True)
    start_time = Column('start_time', Time, nullable=False)
    end_time = Column('end_time', Time, nullable=False)
    # schedule_enabled = Column('schedule_enabled', Boolean, nullable=False)

    decision = Column('decision_code', Enum(EnumDecisionCodes), nullable=False) 
    reason = Column('reason_code', Enum(EnumReasonCodes), nullable=False)
    
class RpiPinMapper(Base):
    __tablename__ = "pin_mapper"
    
    id = Column('id', Integer, primary_key=True)
    
    # Which one of the 1-8 relay pins
    relay_id = Column("relay_id", Integer, nullable=False, unique=True)

    # Maps a zone to a relay pin
    zone_id = Column('zone_id', Integer, ForeignKey('zone.id'), nullable=True, unique=True)
    zone=relationship("Zone", back_populates="pin_config")

    # Maps a relay pin to a raspberry pi pin
    rpi_pin = Column('rpi_pin', Integer, nullable=False, unique=True)

# TODO: Add table for system settings (location, safety shutoff, auto-disable if safety shutoff was invoked, alerting)
# TODO: Add a table to handle errors (e.g. Zone does not have a mapped pin??)
# TODO: Add table to handle ActivationHistory (activated, time activated, start_time, end_time, zone relationship). Consider correlation with decision history? maye the id from the decision is input to the actiation history?
# TODO: Create a table to support notifications configuration (URLS, what to notify on)

class EnumLogLevel(enum.Enum):
    DEBUG = 0
    INFO = 1
    WARN = 2
    ERROR = 3

class Logs(Base):
    __tablename__ = "logs"
    id = Column('id', Integer, primary_key=True)
    datetime = Column('timestamp', DateTime, default=datetime.now())
    level = Column('level', Enum(EnumLogLevel), nullable=False)
    component = Column('component', String(50), nullable=True)
    message =  Column('message', String(500), nullable=False)

# ###########################
# Event triggers go below
# ##########################
@event.listens_for(RpiPinMapper.__table__, 'after_create')
def after_create(target, connection, **kw):
    # TODO: Add all the relays 
    # connection.session.add(RpiPinMapper(relay_id=1, rpi_pin=2))
    connection.execute("Insert into pin_mapper (relay_id, rpi_pin) VALUES (1,20)")
    connection.execute("Insert into pin_mapper (relay_id, rpi_pin) VALUES (2,14)")
    connection.close()
    # connection.session.commit()

#      enabled = Column(Boolean)
# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///sqlalchemy_example.db?check_same_thread=False')


# # Create all tables in the engine. This is equivalent to "Create Table"
# # statements in raw SQL.
Base.metadata.create_all(engine)