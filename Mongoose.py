import sys
import ac
import acsys
import os
import os.path
import platform
import math
import datetime
import json


#Picking between 64bit or 32bit libraries for the physics modules (fuel etc.)
if platform.architecture()[0] == "64bit":
    sysdir=os.path.dirname(__file__)+'/shared_memory/stdlib64'
else:
    sysdir=os.path.dirname(__file__)+'/shared_memory/stdlib'

pymondir = 'C:\\Users\\Kobe\\AppData\\Local\\Programs\\Python\\Python36\\lib\\site-packages'
sys.path.insert(0, sysdir)
os.environ['PATH'] = os.environ['PATH'] + ";."
sys.path.insert(0, pymondir)
os.environ['PATH'] = os.environ['PATH'] + ";."

path1 = str(sys.path)

#Importing the info module, which inclued fuel info 
from shared_memory.sim_info import info

#import pymongo

#Database Setup
# uri = "mongodb://ac-mongo:upNGPuyK07l8RwB45uJSY3idFwej15o5elp6GTZo9jCCosAppidDHVexs4pgNwZMzO333KWlzWHOFdRN6IvfIg==@ac-mongo.documents.azure.com:10255/?ssl=true&replicaSet=globaldb"
# MongoConnect = pymongo.MongoClient(uri)
# db = MongoConnect.ACMods
# collection = db.TestData

#Global variables
l_lapcount=0
lapcount=0
l_speed=0
tick=0
mins=0
secs=0
tenths=0

#Setting up multilevel dictionaries
class AutoTree(dict):
#"""Dictionary with unlimited levels"""
     def __missing__(self, key):
        value = self[key] = type(self)()
        return value

session = AutoTree()

#Output file name and directory definition
sessionstarttime = datetime.datetime.now().strftime(' %b, %d, %Y %H %M %S')
targetdir = os.path.dirname(__file__)+'/Logs/'
targetname = "{d}Session from {t}.json".format(d=targetdir,t=sessionstarttime)
targetfile = open(targetname,"w")

#Main Assetto Corsa function, builds the App Window and the labels associated with it
def acMain(ac_version):
    global l_lapcount, targetdir, path, tick, session, sessionstarttime, path1
    
    tick=ticker() #set the global variable to be a ticker, see the class below
    
    appWindow = ac.newApp("Mongoose") 
    ac.setSize(appWindow, 250, 200)
    
    ac.log(path1)
    l_lapcount = ac.addLabel(appWindow, "Laps: {}".format(0));
    ac.setPosition(l_lapcount, 3, 30)
    
    session['SessionDate'] = sessionstarttime
    
    return "Mongoose"
    
#Main update function for Assetto Corsa, it runs the enclosed code every DeltaT - I think DeltaT = 1/60 of a second
def acUpdate(deltaT):
    global l_lapcount, l_speed, lapcount, targetfile, tick, mins, secs, tenths, session, logfile
    
    if tick.tack(deltaT):  #does not bother CPU with unnecessary updates, basically exists the update function call if time is less than value specified in ticker()
        return
    
    tenths += 1
    if tenths > 9:
        secs += 1
        tenths = 0
    if secs > 59:
        mins += 1
        secs = 0
        
    # Convert time counters to strings for use as key/value pairs
    strmins = str(mins)
    strsecs = str(secs)
    strtenths = str(tenths)
        
    laps = ac.getCarState(0, acsys.CS.LapCount)
    speed = round(ac.getCarState(0, acsys.CS.SpeedMPH),2)
    currenttime = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-4] #gets the current system clock down to the hundredth of a second (if [-4])

    # Data Logging
    session[strmins][strsecs][strtenths]['speed'] = "{} MPH".format(speed)
    
    #For Updating "Laps" Label
    if laps > lapcount:
        lapcount = laps
        ac.setText(l_lapcount, "Laps: {}".format(lapcount)) #updates the label in the App Window defined on acMain
    
#-----------------------
# ticker function, to determine update rate
#--------------------
class ticker:
    def __init__(self):
        self.ticktimer = 0.0
        self.ticktime = 0.0
        self.tickrate = 0.1 #update rate in seconds
   
    def tack(self,deltaT):
        self.ticktime += deltaT
        self.ticktimer += deltaT
        if self.ticktime >= self.tickrate:
            self.ticktime = self.ticktime % self.tickrate
            return False
        else:
            return True
   
    def debuginfo(self):
        return "ticktimer: %s ticktime: %s tickrate: %s" % (self.ticktimer, self.ticktime, self.tickrate)
        
def acShutdown():
    global targetfile, session, logfile
    #json.dump(session,targetfile, indent=4) #dumps entire session dictionary into a local JSON file
    #collection.insert_one(session)
    #MongoConnect.close()

