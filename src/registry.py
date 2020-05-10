import json
import requests
from db import DB

class Registry(object):

 def __init__(self):
  self.db = DB()

 def __prepareRegisterData(self,regInfos):
  json_resources = open('resources.json','r')
  local_resources = json.load(json_resources)

  for topic in local_resources:
    try:
      local_resources[topic] = regInfos[topic]
    except:
      local_resources[topic] = None
  data_resource={'data':local_resources}	
  print('Dados p Registro')
  print(data_resource)
  print('\n')
  return data_resource

 def __requestRegisterIC(self,localId,regInfos):
   headers= {
     'Content-type': 'application/json',
   }

   data_resource = self.__prepareRegisterData(regInfos)

   print("Registering on InterSCity")
   #response = requests.post ('http://localhost:8000/adaptor/resources', data = json.dumps(data_resource), headers=headers)
   print("Registered")
   #dict_response = json.loads(response.text)
   dict_response={'data':{'uuid':1234}}
   try:
     capabilities = regInfos['capabilities']
     capabilities = json.dumps(capabilities)
     sensoruuid = dict_response['data']['uuid']
     dbIds = self.db.registerDB(localId,sensoruuid,capabilities)
   except:
     dbIds = False
     print('Response error')

   return dbIds

 def registerResourceIC(self,localId,regInfos):
   print("Registry started")
   dbIds = False
   dbIds = self.db.verifyDB(localId)
   if(dbIds == False):
     print("id not on db!")
     dbIds = self.__requestRegisterIC(localId, regInfos)
   else:
     print("id is already in the db")

   return dbIds






