import sys
import ac
import acsys
import os
import os.path
import platform
import math

if platform.architecture()[0] == "64bit":
    sysdir=os.path.dirname(__file__)+'/shared_memory/stdlib64'
else:
    sysdir=os.path.dirname(__file__)+'/shared_memory/stdlib'
sys.path.insert(0, sysdir)
os.environ['PATH'] = os.environ['PATH'] + ";."
 
from shared_memory.sim_info import info

l_lapcount=0
lapcount=0
l_speed=0
topspeed=0
l_fuel=0
fuel=0
LTR_TO_GAL_CONVERSION = 0.26174

def acMain(ac_version):

    global l_lapcount, l_speed, l_fuel, topspeed
    appWindow = ac.newApp("Mongoose")
    
    ac.setSize(appWindow, 250, 200)

    #ac.log(print("Hello Assetto Corsa log!")
    #ac.console("Hello Assetto Corsa console!")
    
    l_speed = ac.addLabel(appWindow, "Highest Top Speed: {}".format(topspeed));
    l_lapcount = ac.addLabel(appWindow, "Laps: 0");
    l_fuel = ac.addLabel(appWindow, "Fuel: 0");
    ac.setPosition(l_lapcount, 3, 30)
    ac.setPosition(l_speed, 3, 60)
    ac.setPosition(l_fuel, 3, 90)
    
    return "Lap Counter"
    
def acUpdate(deltaT):
    global l_lapcount, l_speed, lapcount, topspeed, l_fuel, fuel, LTR_TO_GAL_CONVERSION
    laps = ac.getCarState(0, acsys.CS.LapCount)
    speed = ac.getCarState(0, acsys.CS.SpeedMPH)
    fuel = info.physics.fuel * LTR_TO_GAL_CONVERSION
    ac.setText(l_fuel, "Current Fuel Level: {} gal".format(round(fuel,2)))
    
    if speed > topspeed:
        topspeed = round(speed,2)
        ac.setText(l_speed, "Highest Top Speed: {} MPH".format(topspeed))
        
    if laps > lapcount:
        lapcount = laps
        ac.setText(l_lapcount, "Laps: {}".format(lapcount))