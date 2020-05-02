import json
import requests
from db import DB

class Registry(object):

	def __init__(self):
		pass

	def __prepareRegisterData(self,sensorLocalID):
		json_resources = open('resources.json','r')
		local_resources = json.load(json_resources)

		data_resource={'data':local_resources[sensorLocalID]}		
		return data_resource

	def __requestRegisterIC(self,sensorLocalID):
		headers= {
			'Content-type': 'application/json',
		}

		data_resource = __prepareRegisterData(sensorLocalID)

		print("Cadastrando resource na plataforma")
		response = requests.post ('http://localhost:8000/adaptor/resources', data = json.dumps(data_resource), headers=headers)
		print("Cadastro na InterSCity Concluido")
		dict_response = json.loads(response.text)
		dbIds = DB.registerDB((sensorLocalID,dict_response['data']['uuid']))

		return dbIds

	def registerResourceIC(self,sensorData):
		dbIds = DB.verifyDB(sensorData['localId'])
		if(dbIds == False):
			dbIds = __requestRegisterIC(sensorData['localId'])
		return dbIds






