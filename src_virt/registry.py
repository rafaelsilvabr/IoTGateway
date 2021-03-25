import json
import requests
from db import DB

class Registry(object):

 def __init__(self):
  self.db = DB()

# TODO reimplementar
 def __prepareRegisterData(self,regInfos):
  json_resources = open('resources.json','r')
  local_resources = json.load(json_resources)

  for topic in local_resources:
    try:
      local_resources[topic] = regInfos[topic]
    except:
      local_resources[topic] = None
  data_resource={'data':local_resources}	
  return data_resource

 def __requestRegisterIC(self,localId,regInfos):
   headers= {
     'Content-type': 'application/json',
   }

   #data_resource = self.__prepareRegisterData(regInfos)
   data_resource = regInfos

   print('\n')
   print('Dados p Registro')
   print(data_resource)
   print('\n')

   print("Registering on InterSCity")
   #response = requests.post ('http://34.95.255.97:8000/adaptor/resources', data = json.dumps(data_resource), headers=headers)
   #print("Registered:")
   #print(response)

  # dict_response={'data':{'uuid':1234}} #comentar essa linha apenas quando  linha 37 estiver comentada
   try:
     #print(response.text)
     #print('\n')
     #dict_response = json.loads(response.text)
     #capabilities = regInfos['capabilities']
     #capabilities = json.dumps(capabilities)
     #sensoruuid = dict_response['data']['uuid']
     sensoruuid = "54321"
     dbIds = self.db.registerDB(localId,sensoruuid,'empty') #adicionar capabilities no registro local
   except:
     dbIds = False
     print('Response error')

   return dbIds

 def registerResourceIC(self,localId,regInfos):
   print("Registry started")
   dbIds = False
   dbIds = self.db.verifyDB(localId)
   if(dbIds == False):
     print("id not in db!")
     dbIds = self.__requestRegisterIC(localId, regInfos)
   else:
     print("id is already in db")

   return dbIds
   
 def consultRegister(self,localId):
   dbIds = self.db.verifyDB(localId)
   return dbIds  

 def getCoapSensors(self):
   sensors = self.db.getCoap()
   return sensors

 def saveCoapSensorsInfo(self,receivedData):
   print('reg,save coap')
   sensors = self.db.regCoap(receivedData)
   return sensors