from create_db import Sensors

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

 def registerDB(self, sensorLocalID, uuid , capabilities):
  dbIds = False
  try:
   dbIds = Sensors.create(localid=sensorLocalID,uuid=uuid, capabilities = capabilities)
   print("LocalId and UUID linked in db")
  except:
   print("Error registering in db")
  return dbIds
