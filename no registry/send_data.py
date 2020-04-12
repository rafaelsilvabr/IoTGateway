import requests
import json
from create_db import Sensors
  
def send_data(received_data,local_sensor, data_resource):
	json_capabilities = open('capabilities.json','r')
	local_capabilities = json.load(json_capabilities)

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

	response = requests.post ('http://localhost:8000/adaptor/resources/' + local_sensor.uuid + '/data', data = json.dumps(p_data),headers=headers)
	print('Dados Enviados')
	print(response.text)
	print('\n')