from db_schema import Base, Zone, TemperatureRule, RainRule
from pprint import *
from sqlalchemy.inspection import inspect
from sqlalchemy import *
engine = create_engine('sqlite:///sqlalchemy_example.db')
Base.metadata.bind = engine
from sqlalchemy.orm import sessionmaker
DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()
allZones = session.query(Zone).all()
metadata = MetaData()



for zone in session.query(Zone).all():
    # print [cname for cname in zone.__dict__.keys()]
    # pprint(vars(zone))
    # pprint(vars(zone.temperature_rule))
    # pprint(vars(zone.rain_rule))
    # for sch in zone.schedules:
        # pprint(vars(sch))
   

    # print("Name: " + zone.name + "\n")
    # if zone.temperature_rule is not None:
    #     print("Temp Rules - Lower Limit:" + str(zone.temperature_rule.lower_limit))
    #     print("Temp Rules - Upper Limit:" + str(zone.temperature_rule.upper_limit))
    
    # print("Schedule: \n")

    # for sch in zone.schedules:
    #     print("->id="+ str(sch.id))
    #     print("--->startTime=" + str(sch.start_time))
    #     print("--->endTime=" + str(sch.end_time))
    # print(zone.environment)
    
# for rule in tempRules:
#     print(rule.lower_limit)
#     print(rule.upper_limit)


