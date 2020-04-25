import json
import requests
from create_db import Sensors
from send_data import send_data

def register (received_data):

	json_resources = open('resources.json','r')~~
	local_resources = json.load(json_resources)~~

	data_resource={'data':local_resources[received_data['localId']]}~

	try:	
		local_sensor=Sensors.get(Sensors.localid==received_data['localId']).get() 
		print('Sensor ja cadastrado na db')
	except: 
		print("Cadastrando resource na plataforma")
~		response = requests.post ('http://localhost:8000/adaptor/resources', data = json.dumps(data_resource),headers=headers)
		print("Cadastro na InterSCity Concluido")
		dict_response = json.loads(response.text)
		local_sensor = Sensors.create(localid=received_data['localId'],uuid=dict_response['data']['uuid'])
		print("LocalId e UUID vinculados na db")

	msg={'registred':True
	}		
	return msg