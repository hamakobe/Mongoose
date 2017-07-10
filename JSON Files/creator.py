import json
import os
import datetime

#Output file name and directory definition
sessionstarttime = datetime.datetime.now().strftime(' %b, %d, %Y %H %M %S')
targetdir = '../JSON Files/'
targetname = "{d}Session from {t}.json".format(d=targetdir,t=sessionstarttime)

session = {}
session['start']='7/12/2017 16:14:56.12'

for mins in range(60):
  session[mins]={}
  for secs in range(60):
    session[mins][secs]={}
    for tenths in range(10):
      session[mins][secs][tenths]={}
      session[mins][secs][tenths]['elapsed_time']="{m}:{s}.{t}".format(m=mins,s=secs,t=tenths)
      session[mins][secs][tenths]['speed']=mins*mins*tenths*(0.001)
      session[mins][secs][tenths]['psi']={'lf':30,'rf':28,'lr':31,'rr':29,'allavg':(30+28+31+29)/4}
      session[mins][secs][tenths]['temp']={'lf':80,'rf':82,'lr':81,'rr':89,'allavg':(80+82+81+89)/4}
      session[mins][secs][tenths]['wheelweight']={'lf':300,'rf':208,'lr':301,'rr':209,'allavg':(300+208+301+209)/4}
    

#sessionjson = json.dumps(session)
#print(sessionjson)
with open(targetname, 'w') as fp:
    json.dump(session, fp)

fileinfo = os.stat(targetname)
filesizeMB = round(fileinfo.st_size*1e-6,2)
print("{} MB".format(filesizeMB))