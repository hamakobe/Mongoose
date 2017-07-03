import sys
import ac
import acsys
import os
import os.path
import platform
import math
import datetime

#Picking between 64bit or 32bit libraries for the physics modules (fuel etc.)
if platform.architecture()[0] == "64bit":
    sysdir=os.path.dirname(__file__)+'/shared_memory/stdlib64'
else:
    sysdir=os.path.dirname(__file__)+'/shared_memory/stdlib'
sys.path.insert(0, sysdir)
os.environ['PATH'] = os.environ['PATH'] + ";."

#Importing the info module, which inclued fuel info 
from shared_memory.sim_info import info

#Global variables
l_lapcount=0
lapcount=0
l_speed=0
tick=0

#Output file name and directory definition
sessionstarttime = datetime.datetime.now().strftime(' %b, %d, %Y %H %M %S')
targetdir = os.path.dirname(__file__)+'/Logs/'
targetname = "{d}Session from {t}.txt".format(d=targetdir,t=sessionstarttime)
targetfile = open(targetname,"w")

#Main Assetto Corsa function, builds the App Window and the labels associated with it
def acMain(ac_version):
    global l_lapcount, targetdir, path, tick
    
    tick=ticker() #set the global variable to be a ticker, see the class below
    
    appWindow = ac.newApp("Mongoose") 
    ac.setSize(appWindow, 250, 200)
    
    l_lapcount = ac.addLabel(appWindow, "Laps: {}".format(0));
    ac.setPosition(l_lapcount, 3, 30)
    
    return "Mongoose"
    
#Main update function for Assetto Corsa, it runs the enclosed code every DeltaT - I think DeltaT = 1/60 of a second
def acUpdate(deltaT):
    global l_lapcount, l_speed, lapcount, targetfile, tick

    if tick.tack(deltaT):  #does not bother CPU with unnecessary updates, basically exists the update function call if time is less than value specified in ticker()
        return
     
    laps = ac.getCarState(0, acsys.CS.LapCount)
    speed = ac.getCarState(0, acsys.CS.SpeedMPH)
    currenttime = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-4] #gets the current system clock down to the hundredth of a second (if [-4])
    
    targetfile.write("{c} {s} MPH \n".format(c=currenttime,s=round(speed,2)))
           
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
