import json
import os
import datetime
import pymongo

#Databse Setup
uri = "mongodb://ac-mongo:upNGPuyK07l8RwB45uJSY3idFwej15o5elp6GTZo9jCCosAppidDHVexs4pgNwZMzO333KWlzWHOFdRN6IvfIg==@ac-mongo.documents.azure.com:10255/?ssl=true&replicaSet=globaldb"
MongoConnect = pymongo.MongoClient(uri)
db = MongoConnect.ACMods
collection = db.TestData

#Output file name and directory definition
class AutoTree(dict):
#"""Dictionary with unlimited levels"""
     def __missing__(self, key):
        value = self[key] = type(self)()
        return value

session = AutoTree()
session['session_start'] = datetime.datetime.now().strftime(' %b, %d, %Y %H %M %S')

for mins in range(60):
  for secs in range(60):
    for tenths in range(10):
      strmins = str(mins)
      strsecs = str(secs)
      strtenths = str(tenths)
      
      session[strmins][strsecs][strtenths]['elapsed_time']="{m}:{s}.{t}".format(m=mins,s=secs,t=tenths)
      session[strmins][strsecs][strtenths]['speed']=mins*mins*tenths*(0.01)
      #session[strmins][strsecs][strtenths]['psi']={'lf':30,'rf':28,'lr':31,'rr':29,'allavg':(30+28+31+29)/4}
      #session[strmins][strsecs][strtenths]['temp']={'lf':80,'rf':82,'lr':81,'rr':89,'allavg':(80+82+81+89)/4}
      #session[strmins][strsecs][strtenths]['wheelweight']={'lf':300,'rf':208,'lr':301,'rr':209,'allavg':(300+208+301+209)/4}
      
collection.insert_one(session)

#print(session)

MongoConnect.close()

