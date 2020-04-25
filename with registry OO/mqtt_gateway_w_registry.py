import paho.mqtt.client as mqtt
import json
from register import register
from send_data import send_data

#define json header
headers= {
	'Content-type': 'application/json',
}

#define mqtt parameters
MQTT_ADDRESS = "soldier.cloudmqtt.com"
MQTT_PORT = 10514
MQTT_TIMEOUT = 1
TOPIC = "test5"
client = mqtt.Client()

#receives data from a sensor and sends it to the  InterSCity platform
def on_message(client,userdata,msg):
	print("Mensagem Recebida :")
	print (msg.payload)
	received_data = json.loads(msg.payload)
	
	#the register method registers and calls the send_data method
	if(received_data['registred']==False):
		msg=register(received_data) ~~
		client.publish(received_data['localId'],json.dumps(msg),qos=1,retain=True)	
		print('Confirmacao enviada ao sensor')
	else:
		send_data(received_data) ~~

#mqtt connection
client.username_pw_set("ctuqpqym","Xk5GNcWqcmZG")
client.connect(MQTT_ADDRESS,MQTT_PORT,MQTT_TIMEOUT)
client.subscribe(TOPIC)

client.on_message = on_message
client.loop_forever()