import paho.mqtt.client as mqtt
import json

MQTT_ADDRESS = "soldier.cloudmqtt.com"
MQTT_PORT = 10514
MQTT_TIMEOUT = 60

client = mqtt.Client()

client.username_pw_set("ctuqpqym","Xk5GNcWqcmZG")
client.connect(MQTT_ADDRESS,MQTT_PORT,MQTT_TIMEOUT)

msg={'localId':'sensor01',
     'temperature': 40,
     'humidity': 50}

#client.publish("test","helloworld",qos=1,retain=True)
client.publish("test4",json.dumps(msg),qos=1,retain=True)

