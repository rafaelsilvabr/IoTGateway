import json
import requests
from db import DB

class Registry(object):

	def __init__(self):
		self.db = DB()

	def __prepareRegisterData(self,sensorLocalID):
		json_resources = open('resources.json','r')
		local_resources = json.load(json_resources)

		data_resource={'data':local_resources[sensorLocalID]}		
		return data_resource

	def __requestRegisterIC(self,sensorLocalID):
		headers= {
			'Content-type': 'application/json',
		}

		data_resource = self.__prepareRegisterData(sensorLocalID)

		print("Registering on InterSCity")
		response = requests.post ('http://localhost:8000/adaptor/resources', data = json.dumps(data_resource), headers=headers)
		print("Registered")
		dict_response = json.loads(response.text)

		try:
			sensoruuid = dict_response['data']['uuid']
			dbIds = self.db.registerDB(sensorLocalID,sensoruuid)
		except:
			dbIds = False
			print('Response error')

		return dbIds

	def registerResourceIC(self,sensorData):
		print("Registry started")
		dbIds = False
		dbIds = self.db.verifyDB(sensorData['localId'])

		if(dbIds == False):
			print("id not on db!")
			dbIds = self.__requestRegisterIC(sensorData['localId'])
		else:
			print("id based on db")

		return dbIds






