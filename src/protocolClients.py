import json
#from abc import ABC, abstractmethod
from registry import Registry
from sender import Sender
import paho.mqtt.client as mqtt
import timeit 

class ProtocolClient (object):
	def __init__(self,gatewayId):
		self.gatewayId = gatewayId
		self.reg = Registry()
		self.send = Sender()

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
		start = timeit.timeit()
		print("Received a Message")
		receivedData = json.loads(msg.payload)
		
		#check type register or pub
		if(receivedData['registred']==False):
			dbIds = self.reg.registerResourceIC(receivedData)
			if(dbIds != False):
				#send confirmation to client
				confirm={'registred':True
				}
				client.publish(receivedData['localId'],json.dumps(confirm),qos=1,retain=True)	
		else:
			self.send.sendDataIC(receivedData)
			
		end = timeit.timeit()
		print('Runtime:')
		print(end - start)
		print('\n')		

	def startListening (self,mqttBrokerUser,mqttBrokerPassword):
		self.mqttClient = mqtt.Client()
		self.mqttClient.username_pw_set(mqttBrokerUser,mqttBrokerPassword)
		self.mqttClient.connect(self.mqttAddress,self.mqttPort,self.mqttTimeout)
		self.mqttClient.subscribe(self.mqttTopic)	
		print('Connected')
		self.mqttClient.on_message = self.on_message	
		self.mqttClient.loop_forever()

class MqttClassWithoutReg (ProtocolClient):
	def __init__(self, gatewayId, mqttAddress, mqttPort, mqttTimeout, mqttTopic):
		ProtocolClient.__init__(self,gatewayId)
		self.mqttAddress = mqttAddress
		self.mqttPort = mqttPort
		self.mqttTimeout = mqttTimeout
		self.mqttTopic = mqttTopic

	def on_message(self,client,userdata,msg):
		start = timeit.timeit()
		print("Received a Message")
		receivedData = json.loads(msg.payload)
		
		#check type register or pub
		dbIds = self.reg.registerResourceIC(receivedData)
		if(dbIds != False):
			#send data to IC
			self.send.sendDataIC(receivedData)
			
		end = timeit.timeit()
		print('Runtime:')
		print(end - start)
		print('\n')		

	def startListening (self,mqttBrokerUser,mqttBrokerPassword):
		self.mqttClient = mqtt.Client()
		self.mqttClient.username_pw_set(mqttBrokerUser,mqttBrokerPassword)
		self.mqttClient.connect(self.mqttAddress,self.mqttPort,self.mqttTimeout)
		self.mqttClient.subscribe(self.mqttTopic)	
		print('Connected')
		self.mqttClient.on_message = self.on_message	
		self.mqttClient.loop_forever()


