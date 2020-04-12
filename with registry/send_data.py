import requests
import json
from create_db import Sensors
  
def send_data(received_data):
	json_capabilities = open('capabilities.json','r')
	local_capabilities = json.load(json_capabilities)

	json_resources = open('resources.json','r')
	local_resources = json.load(json_resources)

	data_resource={'data':local_resources[received_data['localId']]}

	try:	
		local_sensor=Sensors.get(Sensors.localid==received_data['localId']).get() 
		print('Sensor ja cadastrado na db')
	except: 
		print('error')
		exit()

	#monta o json para envio de dados
	dict_capabilitie = {}
	for capabilitie in data_resource['data']['capabilities']:
		for capabilitie_data in local_capabilities[capabilitie]:
			#print(capabilitie_data)
			for loc_data in capabilitie_data:
				#print (loc_data)
				capabilitie_data[loc_data]=received_data[loc_data]
		dict_capabilitie[capabilitie] = local_capabilities[capabilitie]	
	p_data = {"data":dict_capabilitie}
	print(p_data)

#	response = requests.post ('http://localhost:8000/adaptor/resources/' + local_sensor.uuid + '/data', data = json.dumps(p_data),headers=headers)
	print('Dados Enviados IC')
	print(response.text)
	print('\n')