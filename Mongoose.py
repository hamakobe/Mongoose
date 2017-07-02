import sys
import ac
import acsys
import os
import os.path
import platform
import math
import datetime
import time

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
sessionstarttime = datetime.datetime.now().strftime(' %b, %d, %Y %H %M %S')
targetdir = os.path.dirname(__file__)+'/Logs/'
targetname = "{d}Session from {t}.txt".format(d=targetdir,t=sessionstarttime)
targetfile = open(targetname,"w")

def acMain(ac_version):

    global l_lapcount, targetdir
    appWindow = ac.newApp("Mongoose")
    
    ac.setSize(appWindow, 250, 200)
    
    #ac.console("The target file name is: {}".format(targetname))
    
    l_lapcount = ac.addLabel(appWindow, "Laps: 0");
    ac.setPosition(l_lapcount, 3, 30)
    ac.setPosition(l_speed, 3, 60)
    
    return "Lap Counter"
    
def acUpdate(deltaT):
    global l_lapcount, l_speed, lapcount, targetfile
    laps = ac.getCarState(0, acsys.CS.LapCount)
    speed = ac.getCarState(0, acsys.CS.SpeedMPH)
    currenttime = 0
    
    for i in range(600):
        time.sleep(1 - time.monotonic() % 5)
        currenttime = datetime.datetime.now().strftime('%H:%M:%S')
        targetfile.write("{c} {s} MPH \n".format(c=currenttime,s=speed))
           
    if laps > lapcount:
        lapcount = laps
        ac.setText(l_lapcount, "Laps: {}".format(lapcount))