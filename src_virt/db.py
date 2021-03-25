from create_db import Sensors
import json

class DB(object):
 def __init__(self):
  pass

 def verifyDB(self, sensorLocalID):
  print('Search for id in db')
  dbIds = False
  try:	
   local_sensor=Sensors.get(Sensors.localid == sensorLocalID).get() 
   print('Sensor already registered in db')
   dbIds = local_sensor
  except: 
   print('Sensor not registered')
  return dbIds

 def registerDB(self, sensorLocalID, uuid, lastdata):
  dbIds = False
  try:
   dbIds = Sensors.create(localid=sensorLocalID, uuid=uuid, lastdata=lastdata)
   print("LocalId and UUID linked in db")
  except:
   print("Error registering in db")
  return dbIds

 def updateDB(self,sensorLocalID,lastdata):
  dbIds = False
  try:
   print(sensorLocalID)
   print(lastdata)
   dbIds = Sensors.get(Sensors.localid == sensorLocalID).get()
   dbIds.lastdata = lastdata
   dbIds.save()
   print("updated in db")
  except:
   print("update failed")

 def getCoap(self):
  print("Getting Coap Sensor")
  jsonSensors = open('coapSensors.json','r')
  coapSensors = json.load(jsonSensors)
  print(coapSensors)
  print(type(coapSensors))
  return coapSensors

 def regCoap(self,receivedData):
  print("Register Coap Sensor")
  sensors = self.getCoap()
  print(type(receivedData))
  print(receivedData)
  sensors[receivedData['localid']] = {"address":receivedData["address"], "timeout":receivedData["timeout"]}

  jsonSensors = open('coapSensors.json','w')
  json.dump(sensors,jsonSensors)
  print('Salvo')