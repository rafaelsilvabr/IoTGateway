import json
import requests
from create_db import Sensors
from send_data import send_data

class Registry(object):
	def __init__(self):
		pass

	def registerResourceIC(self,sensorLocalID):
		headers= {
			'Content-type': 'application/json',
		}

		json_resources = open('resources.json','r')
		local_resources = json.load(json_resources)

		data_resource={'data':local_resources[sensorLocalID]}

		print("Cadastrando resource na plataforma")
		response = requests.post ('http://localhost:8000/adaptor/resources', data = json.dumps(data_resource), headers=headers)
		print("Cadastro na InterSCity Concluido")
		dict_response = json.loads(response.text)
		dbIds = self.createInDb(sensorLocalID,dict_response['data']['uuid'])

		return dbIds

	def createInDb(self, sensorLocalID, uuid):
		dbIds=False
		try:
			dbIds = Sensors.create(localid=sensorLocalID,uuid=uuid)
			print("LocalId e UUID vinculados na db")
		except:
			print("Erro ao cadastrar na db")
		return dbIds

	def getInDb(self, sensorLocalID):
		dbIds = False
		try:	
			local_sensor=Sensors.get(Sensors.localid==sensorLocalID).get() 
			print('Sensor ja cadastrado na db')
			dbIds = local_sensor
		except:
			print('Sensor nao cadastrado')

		return dbIds
