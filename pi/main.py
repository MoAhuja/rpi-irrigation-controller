import threading
from configparser import ConfigParser

def initialize():
    readConfig()
    printConfig()
    threading.Timer(1, heartbeat).start()

def readConfig():
    global config
    config = ConfigParser()
    config.read('pi/configuration.ini')
    
    
def printConfig():
    global config
    print("Zone 1 PIN = " + config['ZONE']['ZONE_1_PIN'])
    print("Zone 2 PIN = " + config['ZONE']['ZONE_2_PIN'])
    print("Zone 3 PIN = " + config['ZONE']['ZONE_3_PIN'])
    print("Zone 4 PIN = " + config['ZONE']['ZONE_4_PIN'])

def heartbeat():
    print ("Heartbeat")
    
    # Set the timer to run the heartbeat function in 1 second
    # threading.Timer(1, heartbeat).start()