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

		print("Cadastrando resource na plataforma")
		response = requests.post ('http://localhost:8000/adaptor/resources', data = json.dumps(data_resource), headers=headers)
		print("Cadastro na InterSCity Concluido")
		dict_response = json.loads(response.text)

		#tratamento de erro aqui
		try:
			sensoruuid = dict_response['data']['uuid']
			dbIds = self.db.registerDB(sensorLocalID,sensoruuid)
			print("Cadastro registrado na db")
		except:
			dbIds = False
			print('Erro ao realizar cadastro')

		return dbIds

	def registerResourceIC(self,sensorData):
		print("Regist Resource Called")
		print("Looking for ids in db")
		dbIds = False
		dbIds = self.db.verifyDB(sensorData['localId'])

		if(dbIds == False):
			print("id not founded, registring on InterSCity")
			dbIds = self.__requestRegisterIC(sensorData['localId'])
		else:
			print("id founded in db")

		return dbIds






