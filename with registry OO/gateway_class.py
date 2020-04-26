import json
import abc
from registry import Registry
from sender import Sender
import paho.mqtt.client as mqtt

class protocolClient (abc.ABC):
	def __init__(self,gatewayId):
		self.gatewayId=gatewayId

	def callRegistry(self,sensorData):
		reg = Registry()
		dbIds = reg.getInDb(sensorData['localId'])
		if(dbIds == False):
			dbIds = reg.registerResourceIC(sensorData['localId'])

	def callSender(self,sensorData):
		send = Sender()
		dbIds = send.verifyDb(sensorData['localId'])
		if(dbIds != False):
			send.sendDataIC(sensorData)

	@abc.abstractmethod
	def receiveData(self):
		pass

class mqttClass (protocolClient):
	def __init__(self, gatewayId, mqttAddress, mqttPort, mqttTimeout, mqttTopic):
	 super().__init__(gatewayId)
	 self.mqttAddress = mqttAddress
	 self.mqttPort = mqttPort
	 self.mqttTimeout = mqttTimeout
	 self.mqttTopic = mqttTopic

	
	




