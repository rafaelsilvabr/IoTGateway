from create_db import Sensors

class DB(object):
 def __init__(self):
  pass

 def verifyDB(self, sensorLocalID):
  print("Loking on db")
  dbIds = False
  try:	
   local_sensor=Sensors.get(Sensors.localid == sensorLocalID).get() 
   print('Sensor ja cadastrado na db')
   dbIds = local_sensor
  except:
   print('Sensor nao cadastrado')
  return dbIds

 def registerDB(self, sensorLocalID, uuid):
  dbIds = False
  try:
   dbIds = Sensors.create(localid=sensorLocalID,uuid=uuid)
   print("LocalId e UUID vinculados na db")
  except:
   print("Erro ao cadastrar na db")
  return dbIds
