import json
from abc import ABCMeta, abstractmethod
from registry import Registry
from sender import Sender
import paho.mqtt.client as mqtt
import timeit 

class ProtocolClient ():
	__metaclass__ = ABCMeta
	def __init__(self,gatewayId):
		self.gatewayId = gatewayId
		self.reg = Registry()
		self.send = Sender()

	@abstractmethod
	def dataProcessing(self):
		pass

#-----------------------------MQTT--------------------------------------------

class MqttClass (ProtocolClient):
	def __init__(self, gatewayId, mqttAddress, mqttPort, mqttTimeout, mqttTopic):
		ProtocolClient.__init__(self,gatewayId)
		self.mqttAddress = mqttAddress
		self.mqttPort = mqttPort
		self.mqttTimeout = mqttTimeout
		self.mqttTopic = mqttTopic

	def dataProcessing(self,client,receivedData):
		#check type of message, with ot without state
		if(receivedData['estado']==True):
			print('Sensor with status identified')
			if(receivedData['registred']==False):
				dbIds = self.reg.registerResourceIC(receivedData['localId'],receivedData['regInfos'])
				if(dbIds != False):
					#send confirmation to client
					confirm={'registred':True
					}
					client.publish(receivedData['localId'],json.dumps(confirm),qos=1,retain=True)	
			else:
				dbIds = self.reg.consultregister(receivedData['localId'])
				if(dbIds!=False):
					self.send.sendDataIC(dbIds,receivedData['data'])
		else:
			print('Sensor without status identified')
			#if is a sensor without state
			dbIds = self.reg.registerResourceIC(receivedData['localId'],receivedData['regInfos'])
			if(dbIds != False):
				#send data to IC
				self.send.sendDataIC(dbIds,receivedData['data'])


	def on_message(self,client,userdata,msg):
		start = timeit.timeit()
		print("Received a Message")
		receivedData = json.loads(msg.payload)
	
		dataProcessing(client,receivedData)		

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

#-----------------------------COAP--------------------------------------------
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapthon.client.helperclient import HelperClient

class CoapClass(ProtocolClient):
	def __init__(self):
		self.port = 5683

	def dataProcessing(self,receivedData):
		#dbIds = self.reg.registerResourceIC(receivedData['localId'],receivedData['regInfos'])
		dbIds = True
		if(dbIds != False):
			jsonSensors = open('coapSensors.json','r')
			coapSensors = json.load(jsonSensors)

			coapSensors[receivedData['localId']] = {'address':receivedData['address'],'timeout':receivedData['timeout']}

			jsonSensors = open('coapSensors.json','w')
			json.dump(coapSensors,jsonSensors)
		else:
			print('erro no cadastro')

	def startListening(self):
		server = CoAPServer("0.0.0.0", 5683)
		try:
			server.listen(10)
		except KeyboardInterrupt:
			print "Server Shutdown"
			server.close()
			print "Exiting..."

	def requestSensorData(self):
		jsonSensors = open('coapSensors.json','r')
		coapSensors = json.load(jsonSensors)

		for sensor in coapSensors:
			self.path = '.well-know/core'
			client = HelperClient(server=(sensor['address'],self.port))
			self.response = client.get(path)	

			#separar dado e requisitalos individualmente



class BasicResource(Resource):
    def __init__(self, name="BasicResource", coap_server=None):
        super(BasicResource, self).__init__(name, coap_server, visible=True,observable=True, allow_children=True)
        self.payload = "GatewayInfos"
        self.resource_type = "rt1"
        self.content_type = "text/plain"
        self.interface_type = "if1"
        self.coapProtocolGClient = CoapClass()

    def render_POST(self, request):
        res = self.init_resource(request, BasicResource())
        print('--------------')
        print(res.payload)
        print('--------------')
        receivedData = json.loads(payload)
        coapProtocolGClient.dataProcessing(receivedData)
        return res

class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port))
        self.add_resource('basic/', BasicResource())
