import paho.mqtt.client as mqtt
import json

#define mqtt parameters
MQTT_ADDRESS = "soldier.cloudmqtt.com"
MQTT_PORT = 10514
MQTT_TIMEOUT = 10
TOPIC = "sensor01"
client = mqtt.Client()

def escrever_json(msg):
    with open('regist_status.json', 'w') as f:
        json.dump(msg, f)

#receives data from a sensor and sends it to the  InterSCity platform
def on_message(client,userdata,msg):
	print("Mensagem Recebida :")
	print (msg.payload)
	received_data = json.loads(msg.payload)
	escrever_json(received_data)


#mqtt connection
client.username_pw_set("ctuqpqym","Xk5GNcWqcmZG")
client.connect(MQTT_ADDRESS,MQTT_PORT,MQTT_TIMEOUT)
client.subscribe(TOPIC)

client.on_message = on_message
client.loop_forever()