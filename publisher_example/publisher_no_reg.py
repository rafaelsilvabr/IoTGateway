import paho.mqtt.client as mqtt
import json
import time

MQTT_ADDRESS = "soldier.cloudmqtt.com"
MQTT_PORT = 10514
MQTT_TIMEOUT = 0.2
LocalId = 'sensor01'
registred = False
TOPIC = LocalId
client = mqtt.Client()
'''
def on_message(client,userdata,msg):
	print(1)
	received_data = json.loads(msg.payload)
	print(received_data)
	if(received_data['registred'] == True):
		registred = True
		print("Confirmacao de Cadastro recebida")
'''	 
client.username_pw_set("ctuqpqym","Xk5GNcWqcmZG")
client.connect(MQTT_ADDRESS,MQTT_PORT,MQTT_TIMEOUT)
#client.subscribe(TOPIC)

while True:
	#print(2)
	file = open('regist_status.json','r')
	regist_status = json.load(file)
	
	print(regist_status)

#	print(3)
	msg={'localId':LocalId,
	     'data':{"humidity":50,"temperature":40},
	     'regInfos':{
		'capabilities':["temperature"],
		'description':'A simple test'},
                'estado': False}
	print(json.dumps(msg))
	client.publish("test5",json.dumps(msg),qos=1,retain=True)	
	print("Dado sem regist enviado")

	time.sleep(MQTT_TIMEOUT)
	#print(5)
