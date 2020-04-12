import json
import requests
from create_db import Sensors
from send_data import send_data
import paho.mqtt.client as mqtt

MQTT_ADDRESS = "soldier.cloudmqtt.com"
MQTT_PORT = 10514
MQTT_TIMEOUT = 1

client = mqtt.Client()
client.username_pw_set("ctuqpqym","Xk5GNcWqcmZG")
client.connect(MQTT_ADDRESS,MQTT_PORT,MQTT_TIMEOUT)

def register (received_data):

	json_resources = open('resources.json','r')
	local_resources = json.load(json_resources)

	data_resource={'data':local_resources[received_data['localId']]}

	try:	
		local_sensor=Sensors.get(Sensors.localid==received_data['localId']).get() 
		print('Sensor ja cadastrado na db')
	except: 
		print("Cadastrando resource na plataforma")
		response = requests.post ('http://localhost:8000/adaptor/resources', data = json.dumps(data_resource),headers=headers)
		print("Cadastro na InterSCity Concluido")
		dict_response = json.loads(response.text)
		local_sensor = Sensors.create(localid=received_data['localId'],uuid=dict_response['data']['uuid'])
		print("LocalId e UUID vinculados na db")


	msg={'registred':True
	}		
	#send_data(received_data,local_sensor, data_resource)
	client.publish(received_data['localId'],json.dumps(msg),qos=1,retain=True)	
	print('Confirmacao enviada ao sensor')