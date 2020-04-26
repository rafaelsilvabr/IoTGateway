import json
#from abc import ABC, abstractmethod
from registry import Registry
from sender import Sender
import paho.mqtt.client as mqtt

class ProtocolClient (object):
	def __init__(self,gatewayId):
		self.gatewayId = gatewayId

	def callRegistry(self,sensorData):
		reg = Registry()
		dbIds = reg.getInDb(sensorData['localId'])
		if(dbIds == False):
			dbIds = reg.registerResourceIC(sensorData['localId'])
		return dbIds

	def callSender(self,sensorData):
		send = Sender()
		dbIds = send.verifyDb(sensorData['localId'])
		if(dbIds != False):
			send.sendDataIC(sensorData)

#	@abstractmethod
	def startListening(self):
		pass

class MqttClass (ProtocolClient):
	def __init__(self, gatewayId, mqttAddress, mqttPort, mqttTimeout, mqttTopic):
		ProtocolClient.__init__(self,gatewayId)
		self.mqttAddress = mqttAddress
		self.mqttPort = mqttPort
		self.mqttTimeout = mqttTimeout
		self.mqttTopic = mqttTopic

	def on_message(self,client,userdata,msg):
		print("Mensagem recebida")
		receivedData = json.loads(msg.payload)

		if(receivedData['registred']==False):
			dbIds = self.callRegistry(receivedData)
			if(dbIds != False):
				confirm={'registred':True
				}
				client.publish(receivedData['localId'],json.dumps(confirm),qos=1,retain=True)	
		else:
			self.callSender(receivedData)

	def startListening (self,mqttBrokerUser,mqttBrokerPassword):
		self.mqttClient = mqtt.Client()
		self.mqttClient.username_pw_set(mqttBrokerUser,mqttBrokerPassword)
		self.mqttClient.connect(self.mqttAddress,self.mqttPort,self.mqttTimeout)
		self.mqttClient.subscribe(self.mqttTopic)	
		print('Connected')
		self.mqttClient.on_message = self.on_message	
		self.mqttClient.loop_forever()




